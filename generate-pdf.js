const puppeteer = require('puppeteer');
const fs = require('fs');

// Komentoriviltä saadut tiedostopolut
const args = process.argv.slice(2);
if (args.length < 2) {
    console.error("Usage: node generate-pdf.js <input.html> <output.pdf>");
    process.exit(1);
}

const inputFilePath = args[0];
const outputFilePath = args[1];

(async () => {
    try {
        const browser = await puppeteer.launch({
            headless: true,
            args: ['--no-sandbox', '--disable-setuid-sandbox'],
        });

        const page = await browser.newPage();

        // Lataa HTML-tiedosto
        const htmlContent = fs.readFileSync(inputFilePath, 'utf8');
        await page.setContent(htmlContent, { waitUntil: 'networkidle2' });

        // Lisää Mermaid-tyylit ja scriptit
        await page.addStyleTag({
            url: 'https://cdnjs.cloudflare.com/ajax/libs/mermaid/9.3.0/mermaid.min.css',
        });

        // Mermaid-renderöinti
        try {
            // Odota 15 sekuntia ja tarkista, löytyykö .mermaid-elementtejä
            await page.waitForSelector('.mermaid', { timeout: 15000 });
            console.log("Mermaid-kaaviot löydetty ja renderöity.");
        } catch (error) {
            console.warn('Mermaid-kaavioita ei löydetty. Jatketaan ilman niitä.');
        }

        // Debug: Tallenna kuvakaappaus
        await page.screenshot({ path: 'debug-screenshot.png', fullPage: true });
        console.log("Debug-kuvakaappaus tallennettu tiedostoon debug-screenshot.png");

        // Luo PDF-tiedosto
        await page.pdf({
            path: outputFilePath,
            format: 'A4',
            printBackground: true,
            margin: {
                top: '40px',
                right: '20px',
                bottom: '40px',
                left: '20px',
            },
        });

        await browser.close();
        console.log(`PDF luotu onnistuneesti: ${outputFilePath}`);
    } catch (error) {
        console.error("Virhe PDF:n luomisessa:", error);
        process.exit(1);
    }
})();
