chrome.action.onClicked.addListener(async (tab) => {
    await chrome.scripting.executeScript({
        target: { tabId: tab.id, allFrames: true },
        files: ["scripts/content.js"],
        
    });
});
