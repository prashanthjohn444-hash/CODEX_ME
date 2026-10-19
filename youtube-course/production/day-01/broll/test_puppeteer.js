const puppeteer = require('puppeteer-core');

(async () => {
    try {
        const browser = await puppeteer.launch({
            executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox']
        });
        const page = await browser.newPage();
        await page.setViewport({ width: 1920, height: 1080 });
        await page.setContent(`<!DOCTYPE html><html><body style="background:#1e1e1e;color:#fff;font-family:sans-serif;display:flex;align-items:center;justify-content:center;height:100vh;"><h1>VS Code Headless Test</h1></body></html>`);
        const buf = await page.screenshot({ type: 'png' });
        await browser.close();
        console.log('SUCCESS! Screenshot captured, bytes:', buf.length);
    } catch (err) {
        console.error('ERROR:', err);
    }
})();

