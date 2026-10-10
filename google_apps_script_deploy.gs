/**
 * Smart Project Manager Assistant (SPMA) - Google Apps Script Web App Wrapper
 * Blue Nile University - Faculty of Engineering 2026
 *
 * Instructions:
 * 1. Open https://script.google.com/ and create a New Project.
 * 2. Paste this code into Code.gs.
 * 3. Create an HTML file named "Index.html" in Google Apps Script and paste the content from backend/app/static/index.html.
 * 4. Click Deploy > New deployment > Select type: Web app.
 * 5. Execute as: Me | Who has access: Anyone.
 * 6. You will get a permanent public link like:
 *    https://script.google.com/macros/s/AKfycb.../exec
 */

function doGet(e) {
  return HtmlService.createTemplateFromFile('Index')
    .evaluate()
    .setTitle('Smart Project Manager Assistant (SPMA) - Blue Nile University')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}
