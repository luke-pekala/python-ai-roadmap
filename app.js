// ─────────────────────────────────────────────────────────────────────────────
// app.js — DocStruct Actions
// Depends on: templates.js, renderForm.js (load those first)
// ─────────────────────────────────────────────────────────────────────────────


// ─────────────────────────────────────────────────────────────────────────────
// getPreviewContent()
//
// Single source of truth for reading the current preview text.
// Both copy and download use this so they never go out of sync.
// ─────────────────────────────────────────────────────────────────────────────
function getPreviewContent() {
  const preview = document.getElementById("preview-output");
  return preview ? preview.textContent : "";
}


// ─────────────────────────────────────────────────────────────────────────────
// copyToClipboard()
//
// Copies the current preview content to the clipboard.
// Button text temporarily becomes "Copied ✓" then reverts after 2 seconds.
// Handles browsers where clipboard API is unavailable (fallback alert).
// ─────────────────────────────────────────────────────────────────────────────
function copyToClipboard() {
  const content = getPreviewContent();
  const btn     = document.getElementById("btn-copy");

  // Nothing to copy
  if (!content.trim()) {
    flashButton(btn, "Nothing to copy", "btn--warn", 1800);
    return;
  }

  // Clipboard API (all modern browsers)
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(content)
      .then(() => {
        flashButton(btn, "Copied ✓", "btn--success", 2000);
      })
      .catch((err) => {
        console.error("Clipboard write failed:", err);
        fallbackCopy(content, btn);
      });
  } else {
    // Older browsers: execCommand fallback
    fallbackCopy(content, btn);
  }
}


// ─────────────────────────────────────────────────────────────────────────────
// fallbackCopy(text, btn)
//
// execCommand-based copy for browsers without navigator.clipboard.
// Creates a temporary off-screen textarea, selects its content, copies it.
// ─────────────────────────────────────────────────────────────────────────────
function fallbackCopy(text, btn) {
  const ta = document.createElement("textarea");

  // Position off-screen so it doesn't cause a layout flash
  ta.style.cssText = "position:fixed;top:-9999px;left:-9999px;opacity:0;";
  ta.value = text;
  document.body.appendChild(ta);

  ta.focus();
  ta.select();

  try {
    const success = document.execCommand("copy");
    flashButton(
      btn,
      success ? "Copied ✓" : "Copy failed",
      success ? "btn--success" : "btn--warn",
      2000
    );
  } catch (err) {
    console.error("execCommand copy failed:", err);
    flashButton(btn, "Copy failed", "btn--warn", 2000);
  } finally {
    document.body.removeChild(ta);
  }
}


// ─────────────────────────────────────────────────────────────────────────────
// flashButton(btn, label, cssClass, duration)
//
// Temporarily changes a button's text and adds a CSS class, then restores
// both after `duration` milliseconds. Handles rapid re-clicks safely by
// clearing any pending restore timer before setting a new one.
// ─────────────────────────────────────────────────────────────────────────────
const _flashTimers = new WeakMap();

function flashButton(btn, label, cssClass, duration) {
  if (!btn) return;

  // Cancel any previous flash still counting down on this button
  if (_flashTimers.has(btn)) {
    clearTimeout(_flashTimers.get(btn));
  }

  const originalLabel = btn.dataset.originalLabel ?? btn.textContent;
  btn.dataset.originalLabel = originalLabel; // persist across rapid clicks

  btn.textContent = label;
  btn.classList.add(cssClass);
  btn.disabled = true;

  const timer = setTimeout(() => {
    btn.textContent = originalLabel;
    btn.classList.remove(cssClass);
    btn.disabled = false;
    _flashTimers.delete(btn);
  }, duration);

  _flashTimers.set(btn, timer);
}


// ─────────────────────────────────────────────────────────────────────────────
// downloadMarkdown()
//
// Downloads the preview content as a .md file.
// Filename format: {template-type}_{YYYY-MM-DD}.md
// e.g. api_reference_2024-06-15.md
// ─────────────────────────────────────────────────────────────────────────────
function downloadMarkdown() {
  const content = getPreviewContent();
  const btn     = document.getElementById("btn-download");

  // Nothing to download
  if (!content.trim()) {
    flashButton(btn, "Nothing to save", "btn--warn", 1800);
    return;
  }

  const filename = buildFilename();
  const blob     = new Blob([content], { type: "text/markdown;charset=utf-8" });
  const url      = URL.createObjectURL(blob);

  // Create a temporary anchor, click it, then clean up
  const anchor      = document.createElement("a");
  anchor.href       = url;
  anchor.download   = filename;
  anchor.style.display = "none";

  document.body.appendChild(anchor);
  anchor.click();
  document.body.removeChild(anchor);

  // Revoke the object URL after a short delay so the download has time to start
  setTimeout(() => URL.revokeObjectURL(url), 10_000);

  flashButton(btn, "Downloaded ✓", "btn--success", 2000);
}


// ─────────────────────────────────────────────────────────────────────────────
// buildFilename()
//
// Returns a safe filename using the active template key + today's date.
// Falls back to "template_{date}.md" if no template is active.
// ─────────────────────────────────────────────────────────────────────────────
function buildFilename() {
  const today       = new Date().toISOString().split("T")[0]; // YYYY-MM-DD
  const templateKey = typeof activeTemplateKey === "string" && activeTemplateKey
    ? activeTemplateKey          // e.g. "api_reference"
    : "template";

  return `${templateKey}_${today}.md`;
  // → e.g. "api_reference_2024-06-15.md"
}


// ─────────────────────────────────────────────────────────────────────────────
// init()
//
// Wires up the template selector dropdown and action buttons.
// Call once the DOM is ready.
// ─────────────────────────────────────────────────────────────────────────────
function init() {
  const selector = document.getElementById("template-selector");
  const copyBtn  = document.getElementById("btn-copy");
  const dlBtn    = document.getElementById("btn-download");

  // Populate the <select> from TEMPLATES keys
  if (selector) {
    // Clear any static placeholder options first
    selector.innerHTML = "";

    Object.entries(TEMPLATES).forEach(([key, tpl]) => {
      const opt   = document.createElement("option");
      opt.value   = key;
      opt.textContent = tpl.label;
      selector.appendChild(opt);
    });

    // Render the first template on load
    renderForm(selector.value);

    // Re-render form when user picks a different template
    selector.addEventListener("change", () => {
      renderForm(selector.value);
    });
  }

  if (copyBtn) copyBtn.addEventListener("click", copyToClipboard);
  if (dlBtn)   dlBtn.addEventListener("click", downloadMarkdown);
}

// Kick off once the DOM is fully parsed
document.addEventListener("DOMContentLoaded", init);
