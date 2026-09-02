/**
 * render_html.js — rasterises a local HTML/SVG file to PNG at a fixed CSS width
 * and a chosen device scale factor, so figures land in the report at >= 150 DPI.
 *
 * Usage: node render_html.js <input.html> <output.png> [cssWidth] [scale]
 */
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const [, , input, output, widthArg, scaleArg] = process.argv;
  if (!input || !output) {
    console.error('Usage: node render_html.js <input.html> <output.png> [cssWidth] [scale]');
    process.exit(1);
  }
  const width = parseInt(widthArg || '900', 10);
  const scale = parseFloat(scaleArg || '3');

  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.setViewport({ width, height: 800, deviceScaleFactor: scale });
  await page.goto('file://' + path.resolve(input).replace(/\\/g, '/'), {
    waitUntil: 'networkidle0',
  });

  const target = await page.$('#figure');
  if (!target) {
    console.error('No element with id="figure" found in ' + input);
    process.exit(1);
  }
  await target.screenshot({ path: output, omitBackground: false });
  await browser.close();
  console.log('rendered ' + output + ' at width=' + width + ' scale=' + scale);
})();
