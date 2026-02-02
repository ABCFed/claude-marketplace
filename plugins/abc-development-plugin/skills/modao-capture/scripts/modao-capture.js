#!/usr/bin/env node
/**
 * 墨刀原型稿抓取工具
 * 支持任意墨刀原型稿链接，自动获取所有页面并生成文档
 *
 * 用法:
 *   node modao-capture.js --url "https://modao.cc/proto/xxx/sharing" --output "$(pwd)"
 *   node modao-capture.js --url "url" --output "/path/to/project" --concurrency 3
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const { Command } = require('commander');

// ============== 命令行参数解析 ==============
const program = new Command();

program
  .version('2.0.0')
  .name('modao-capture')
  .description('墨刀原型稿抓取工具 - 自动获取所有页面并生成文档')
  .option('-u, --url <url>', '墨刀原型稿分享链接 (必填)')
  .option('-c, --concurrency <number>', '并发处理数量', '3')
  .option('-s, --scale <number>', '截图缩放因子 (1-5)', '3')
  .option('-o, --output <dir>', '项目根目录路径 (必填，用于确定输出位置)');

program.parse(process.argv);

const args = program.args;
const opts = program.opts();

// 验证必填参数
const urlIndex = args.findIndex(arg => !arg.startsWith('-'));
const modaoUrlArg = opts.url || (urlIndex >= 0 ? args[urlIndex] : null);

if (!modaoUrlArg) {
  console.error('错误: 必须指定墨刀原型稿链接');
  console.error('');
  console.error('用法:');
  console.error('  node scripts/modao-capture.js --url "https://modao.cc/proto/xxx/sharing" --output "$(pwd)"');
  console.error('');
  console.error('选项:');
  console.error('  -u, --url <url>      墨刀原型稿链接 (必填)');
  console.error('  -c, --concurrency N  并发数量 (默认: 3)');
  console.error('  -s, --scale N        截图缩放因子 1-5 (默认: 3)');
  console.error('  -o, --output <dir>   项目根目录路径 (必填)');
  process.exit(1);
}

// 验证 URL 格式
if (!modaoUrlArg.includes('modao.cc/proto')) {
  console.error('错误: 无效的墨刀链接格式');
  console.error('链接必须包含 "modao.cc/proto"');
  process.exit(1);
}

// 验证输出目录参数
if (!opts.output) {
  console.error('错误: 必须指定项目根目录路径 (--output)');
  console.error('');
  console.error('用法:');
  console.error('  node scripts/modao-capture.js --url "url" --output "$(pwd)"');
  console.error('');
  console.error('提示: 使用 "$(pwd)" 获取当前项目目录');
  process.exit(1);
}

// 配置值
const MODAO_URL = modaoUrlArg;
const CONCURRENCY = parseInt(opts.concurrency, 10);
const SCALE_FACTOR = Math.min(Math.max(parseInt(opts.scale, 10), 1), 5);
const OUTPUT_DIR_BASE = opts.output;

// 输出目录（将在运行时根据画布名称设置）
let OUTPUT_DIR;

// ============== 工具函数 ==============

/**
 * 从墨刀链接中提取 project ID
 */
function extractProjectId(url) {
  const match = url.match(/modao\.cc\/proto\/([^\/]+)/);
  return match ? match[1] : null;
}

/**
 * 从 URL 中提取 screen ID
 */
function extractScreenId(url) {
  const match = url.match(/screen=([^&]+)/);
  return match ? match[1] : null;
}

/**
 * 从 URL 中提取 canvasId
 */
function extractCanvasId(url) {
  const match = url.match(/canvasId=([^&]+)/);
  return match ? match[1] : null;
}

/**
 * 获取演示模式的 screenId（从活动画布元素中获取 data-cid）
 */
async function getScreenIdFromPage(page) {
  return await page.evaluate(() => {
    const el = document.querySelector('.rn-list-item.active.select');
    return el ? el.getAttribute('data-cid') : null;
  });
}

/**
 * 将链接转换为演示模式链接
 */
async function toDeviceModeUrl(page, url) {
  // 如果已经是 device 模式，直接返回
  if (url.includes('view_mode=device')) {
    return url;
  }

  // 从 URL 提取基础信息和 canvasId
  const match = url.match(/modao\.cc\/proto\/([^?]+)\/sharing/);
  if (!match) return url;

  const projectId = match[1];
  const canvasId = extractCanvasId(url);

  // 获取 screenId（第一个页面的 cid）
  const screenId = await getScreenIdFromPage(page);
  if (!screenId) {
    console.log('无法获取 screenId');
    return url;
  }

  // 构建演示模式链接
  return `https://modao.cc/proto/${projectId}/sharing?view_mode=device&screen=${screenId}&canvasId=${canvasId || screenId}`;
}

/**
 * 等待元素加载
 */
async function waitForElement(page, selector, timeout = 10000) {
  try {
    await page.waitForSelector(selector, { timeout });
    await new Promise(r => setTimeout(r, 500));
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * 获取页面列表
 */
async function getPageList(page) {
  return await page.evaluate(() => {
    // 优先使用 #mb-enabled-canvas-list（read_only 模式）
    const items = document.querySelectorAll('#mb-enabled-canvas-list > li, .canvas-scroll-list > ul > li');
    const pages = [];
    items.forEach((li, index) => {
      const titleEl = li.querySelector('.editable-name, .title');
      const title = titleEl?.innerText?.trim() || li.innerText?.trim() || `页面${index + 1}`;
      const dataCid = li.getAttribute('data-cid') || li.querySelector('[data-cid]')?.getAttribute('data-cid');
      if (dataCid) {
        pages.push({
          index: index + 1,
          title: title.replace(/^\d+\s*/, ''), // 移除序号前缀
          canvasId: dataCid
        });
      }
    });
    return pages;
  });
}

/**
 * 获取 div.screen-content 的位置和尺寸
 */
async function getScreenContentBounds(page) {
  return await page.evaluate(() => {
    const el = document.querySelector('div.screen-content');
    if (!el) return null;
    const rect = el.getBoundingClientRect();
    return {
      left: Math.round(rect.left),
      top: Math.round(rect.top),
      width: Math.round(rect.width),
      height: Math.round(rect.height)
    };
  });
}

/**
 * 获取批注列表
 */
async function getAnnotations(page) {
  return await page.evaluate(() => {
    const stickies = document.querySelectorAll('.wSticky');
    return Array.from(stickies).map((el, idx) => {
      const text = el.innerText.trim();
      const lines = text.split('\n').filter(l => l.trim());
      const number = lines[0] || String(idx + 1);
      const content = lines.slice(1).join('\n').trim();
      return { number, content };
    });
  });
}

/**
 * 获取画布标题（项目名称）
 */
async function getCanvasTitle(page) {
  return await page.evaluate(() => {
    // 尝试多种选择器获取画布名称
    const selectors = [
      '.rn-list-item.active.select .editable-span', // read_only 模式的活动画布
      '.project-name',
      '.proto-name',
      '.canvas-title',
      '.header-title',
      '[class*="project"] [class*="name"]',
      '.md-tabs .active'
    ];

    for (const selector of selectors) {
      const el = document.querySelector(selector);
      if (el && el.innerText?.trim()) {
        return el.innerText.trim();
      }
    }

    // 从页面标题获取
    const title = document.title;
    const match = title.match(/^(.+?)(?:\s*[-_|]\s*.+)?$/);
    return match ? match[1].trim() : '未知画布';
  });
}

/**
 * 生成安全的文件夹名称
 */
function sanitizeFolderName(name) {
  if (!name) return 'modao_unknown';
  // 替换Windows和macOS不允许的字符
  const sanitized = name.replace(/[\/\\?%*:|"<>]/g, '_');
  // 移除首尾空格和点
  return sanitized.trim().replace(/^[.]+|[.]+$/g, '');
}

/**
 * 生成安全的文件名
 */
function sanitizeFilename(filename) {
  return filename
    .replace(/[\/\\?%*:|"<>]/g, '_')
    .replace(/\s+/g, '_')
    .trim();
}

/**
 * 并发处理工具函数
 */
function pMap(items, fn, concurrency) {
  return new Promise((resolve) => {
    const results = [];
    let index = 0;
    let active = 0;
    const total = items.length;

    function next() {
      if (index >= total) {
        if (active === 0) resolve(results);
        return;
      }

      while (active < concurrency && index < total) {
        const i = index++;
        active++;
        const item = items[i];

        Promise.resolve(fn(item, i)).then(
          (result) => {
            results[i] = result;
            active--;
            next();
          },
          (err) => {
            results[i] = null;
            active--;
            console.error(`  处理失败: ${err.message}`);
            next();
          }
        );
      }
    }

    next();
  });
}

/**
 * 生成 Markdown 文档
 */
function generateMarkdown(pageInfo, imageFileName, annotations) {
  let md = `# ${pageInfo.title}\n\n`;
  md += `## 原型稿\n`;
  md += `![${pageInfo.title}](./${imageFileName})\n\n`;
  md += `## 批注内容\n`;

  if (!annotations || annotations.length === 0 || (annotations.length === 1 && !annotations[0].content)) {
    md += `该页面暂无批注\n`;
  } else {
    annotations.forEach((ann, idx) => {
      if (!ann.content) return;
      md += `### 批注 ${ann.number || idx + 1}\n\n`;
      md += `**内容**：\n\n${ann.content}\n\n`;
      md += `---\n\n`;
    });
  }

  return md;
}

// ============== 主处理逻辑 ==============

async function processPage(page, pageInfo, screenId, outputDir) {
  const baseUrl = MODAO_URL.split('?')[0];
  const url = `${baseUrl}?view_mode=device&screen=${screenId}&canvasId=${pageInfo.canvasId}`;

  console.log(`\n[${pageInfo.index}/${pageInfo.total}] 访问: ${pageInfo.title}`);
  await page.goto(url, { waitUntil: 'networkidle2', timeout: 30000 });

  // 等待页面加载
  if (!await waitForElement(page, 'div.screen-content')) {
    console.log(`  未找到 div.screen-content，尝试等待画布加载...`);
    await new Promise(r => setTimeout(r, 2000));
  }

  // 设置 viewport
  await page.setViewport({ width: 2560, height: 1440, deviceScaleFactor: SCALE_FACTOR });

  // 触发 Cmd+1 让画布适应屏幕
  await page.keyboard.down('Meta');
  await page.keyboard.press('1');
  await page.keyboard.up('Meta');
  await new Promise(r => setTimeout(r, 1000));

  // 获取 div.screen-content 位置和尺寸
  const bounds = await getScreenContentBounds(page);
  if (!bounds || bounds.width === 0) {
    console.log(`  无法获取 div.screen-content 尺寸`);
    return null;
  }

  console.log(`  位置: (${bounds.left}, ${bounds.top}), 尺寸: ${bounds.width}x${bounds.height}`);

  // 截图
  const safeTitle = sanitizeFilename(pageInfo.title);
  const imageFileName = `${String(pageInfo.index).padStart(2, '0')}_${safeTitle}_图1.png`;
  const imagePath = path.join(outputDir, imageFileName);

  await page.screenshot({
    path: imagePath,
    clip: { x: bounds.left, y: bounds.top, width: bounds.width, height: bounds.height }
  });
  console.log(`  截图: ${imageFileName}`);

  // 获取批注
  const annotations = await getAnnotations(page);
  console.log(`  批注: ${annotations.length} 条`);

  // 生成 Markdown
  const mdContent = generateMarkdown(pageInfo, imageFileName, annotations);
  const mdFileName = `${String(pageInfo.index).padStart(2, '0')}_${safeTitle}.md`;
  const mdPath = path.join(outputDir, mdFileName);
  fs.writeFileSync(mdPath, mdContent);
  console.log(`  文档: ${mdFileName}`);

  return {
    pageInfo,
    imageFileName,
    annotations,
    bounds
  };
}

async function main() {
  console.log('==============================================');
  console.log('            墨刀原型稿抓取工具 v2.0                        ');
  console.log('==============================================\n');
  console.log(`链接: ${MODAO_URL}`);
  console.log(`并发数量: ${CONCURRENCY}\n`);

  const projectId = extractProjectId(MODAO_URL);
  console.log(`项目ID: ${projectId || '未知'}`);

  // 检测系统 Chrome 路径 (macOS)
  const macChromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const executablePath = fs.existsSync(macChromePath) ? macChromePath : undefined;

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: executablePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  try {
    const page = await browser.newPage();

    // 先访问一次获取页面列表和画布名称
    console.log('正在获取页面列表...');
    await page.goto(MODAO_URL, { waitUntil: 'networkidle2', timeout: 30000 });
    await new Promise(r => setTimeout(r, 1500));

    // 获取画布标题并设置输出目录
    const canvasTitle = await getCanvasTitle(page);
    const safeFolderName = sanitizeFolderName(canvasTitle);
    OUTPUT_DIR = path.join(OUTPUT_DIR_BASE, `modao_${safeFolderName}`);
    console.log(`画布名称: ${canvasTitle}`);
    console.log(`输出目录: ${OUTPUT_DIR}\n`);

    // 创建输出目录
    if (!fs.existsSync(OUTPUT_DIR)) {
      fs.mkdirSync(OUTPUT_DIR, { recursive: true });
      console.log(`已创建输出目录\n`);
    }

    // 转换为演示模式链接（如果需要）
    const deviceModeUrl = await toDeviceModeUrl(page, MODAO_URL);
    if (deviceModeUrl !== MODAO_URL) {
      console.log(`已转换为演示模式: ${deviceModeUrl.split('?')[1]}`);
    }

    // 获取所有页面
    const pages = await getPageList(page);
    if (pages.length === 0) {
      console.error('未找到任何页面，请检查链接是否正确');
      return;
    }

    console.log(`找到 ${pages.length} 个页面`);
    console.log(`并发数量: ${CONCURRENCY}\n`);
    console.log('------------------------------------------------------------');

    // 关闭初始页面，准备创建并发页面池
    await page.close();

    // 设置 screenId（优先使用转换后的 URL）
    const screenId = extractScreenId(deviceModeUrl) || extractScreenId(MODAO_URL);

    // 创建多个页面实例用于并发处理
    const pagePool = [];
    for (let i = 0; i < CONCURRENCY; i++) {
      const p = await browser.newPage();
      await p.setViewport({ width: 2560, height: 1440, deviceScaleFactor: SCALE_FACTOR });
      pagePool.push(p);
    }

    // 处理每个页面（并发）
    const pageItems = pages.map((p, i) => ({ ...p, total: pages.length }));

    const results = await pMap(pageItems, async (pageInfo) => {
      // 轮询获取一个页面实例
      const pageIndex = pageInfo.index % pagePool.length;
      const workerPage = pagePool[pageIndex];
      return await processPage(workerPage, pageInfo, screenId, OUTPUT_DIR);
    }, CONCURRENCY);

    // 关闭页面池
    for (const p of pagePool) {
      await p.close();
    }

    // 汇总
    console.log('\n------------------------------------------------------------');
    console.log('\n==============================================');
    console.log('                        处理完成                           ');
    console.log('==============================================\n');

    // 过滤掉 null 结果
    const validResults = results.filter(r => r);

    let totalAnnotations = 0;
    validResults.forEach(r => {
      totalAnnotations += r.annotations.filter(a => a.content).length;
    });

    console.log(`总计: ${validResults.length} 个页面, ${totalAnnotations} 条批注`);
    console.log(`输出: ${OUTPUT_DIR}\n`);

    // 生成索引文件
    let indexContent = `# 墨刀原型稿索引\n\n`;
    indexContent += `**项目ID**: ${projectId || '未知'}\n\n`;
    indexContent += `**链接**: ${MODAO_URL}\n\n`;
    indexContent += `---\n\n`;
    indexContent += `## 页面列表\n\n`;
    indexContent += `| 序号 | 页面 | 批注数 |\n`;
    indexContent += `|------|------|--------|\n`;

    validResults.forEach(r => {
      const annotationCount = r.annotations.filter(a => a.content).length;
      indexContent += `| ${r.pageInfo.index} | [${r.pageInfo.title}](./${r.imageFileName.replace('.png', '.md')}) | ${annotationCount} |\n`;
    });

    fs.writeFileSync(path.join(OUTPUT_DIR, 'README.md'), indexContent);
    console.log(`已生成索引文件: README.md`);

  } finally {
    await browser.close();
  }
}

main().catch(console.error);
