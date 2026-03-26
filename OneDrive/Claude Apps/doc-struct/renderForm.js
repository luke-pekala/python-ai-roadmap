// ─────────────────────────────────────────────────────────────────────────────
// renderForm.js — DocStruct Dynamic Form Renderer
// Depends on: templates.js (TEMPLATES must be loaded first)
// ─────────────────────────────────────────────────────────────────────────────

// Tracks which template is currently active so updatePreview() can access it
let activeTemplateKey = null;

// Fields that get a <textarea> instead of a single-line <input>
const TEXTAREA_FIELDS = new Set([
  "description",
  "summary",
  "prerequisites",
  "auth_header",
]);

// How many rows each textarea gets
const TEXTAREA_ROWS = {
  description:  3,
  summary:      3,
  prerequisites: 3,
  auth_header:  2,
};


// ─────────────────────────────────────────────────────────────────────────────
// renderForm(templateKey)
//
// Reads TEMPLATES[templateKey].fields and injects a complete <form> into
// the #form-area div. Every field fires updatePreview() on input.
// ─────────────────────────────────────────────────────────────────────────────
function renderForm(templateKey) {
  const template = TEMPLATES[templateKey];

  // Guard: unknown key
  if (!template) {
    console.warn(`renderForm: unknown template key "${templateKey}"`);
    return;
  }

  activeTemplateKey = templateKey;

  const formArea = document.getElementById("form-area");
  if (!formArea) {
    console.error('renderForm: no element with id="form-area" found in DOM');
    return;
  }

  // ── Build the form element ──────────────────────────────────────────────
  const form = document.createElement("form");
  form.id = "template-form";
  form.noValidate = true; // we handle validation ourselves in updatePreview()
  // Prevent accidental page reload if user hits Enter
  form.addEventListener("submit", (e) => e.preventDefault());

  // ── One field group per entry in fields[] ──────────────────────────────
  template.fields.forEach((fieldDef) => {
    const group = buildFieldGroup(fieldDef);
    form.appendChild(group);
  });

  // ── Replace whatever was in form-area ──────────────────────────────────
  formArea.innerHTML = "";
  formArea.appendChild(form);

  // ── Trigger an initial preview with empty / default values ─────────────
  updatePreview();
}


// ─────────────────────────────────────────────────────────────────────────────
// buildFieldGroup(fieldDef)
//
// Returns a <div class="field-group"> containing:
//   <label>  — display name + optional required star
//   <input> or <textarea>  — wired to updatePreview on input
// ─────────────────────────────────────────────────────────────────────────────
function buildFieldGroup(fieldDef) {
  const { id, label, placeholder, required } = fieldDef;

  const group = document.createElement("div");
  group.className = "field-group";
  group.dataset.fieldId = id;

  // ── Label ──────────────────────────────────────────────────────────────
  const labelEl = document.createElement("label");
  labelEl.htmlFor = `field-${id}`;
  labelEl.className = "field-label";

  const labelText = document.createTextNode(label);
  labelEl.appendChild(labelText);

  if (required) {
    const star = document.createElement("span");
    star.className = "required-star";
    star.textContent = " *";
    star.setAttribute("aria-label", "required");
    labelEl.appendChild(star);
  }

  group.appendChild(labelEl);

  // ── Input or Textarea (wrapped for StyleGuard focus ring) ──────────────
  const wrap = document.createElement("div");
  wrap.className = "field-input-wrap";

  const control = TEXTAREA_FIELDS.has(id)
    ? buildTextarea(id, placeholder, required)
    : buildInput(id, placeholder, required);

  wrap.appendChild(control);
  group.appendChild(wrap);

  return group;
}


// ─────────────────────────────────────────────────────────────────────────────
// buildInput / buildTextarea
// ─────────────────────────────────────────────────────────────────────────────
function buildInput(id, placeholder, required) {
  const input = document.createElement("input");
  input.type        = "text";
  input.id          = `field-${id}`;
  input.name        = id;
  input.placeholder = placeholder || "";
  input.className   = "field-input";
  if (required) input.required = true;

  input.addEventListener("input", updatePreview);
  return input;
}

function buildTextarea(id, placeholder, required) {
  const ta = document.createElement("textarea");
  ta.id          = `field-${id}`;
  ta.name        = id;
  ta.placeholder = placeholder || "";
  ta.className   = "field-textarea";
  ta.rows        = TEXTAREA_ROWS[id] || 3;
  ta.spellcheck  = true;
  if (required) ta.required = true;

  ta.addEventListener("input", updatePreview);
  return ta;
}


// ─────────────────────────────────────────────────────────────────────────────
// getFormData()
//
// Reads every named control inside #template-form and returns a plain object
// { fieldId: currentValue, ... }
// ─────────────────────────────────────────────────────────────────────────────
function getFormData() {
  const form = document.getElementById("template-form");
  if (!form) return {};

  const data = {};
  const controls = form.querySelectorAll("input[name], textarea[name]");

  controls.forEach((control) => {
    data[control.name] = control.value.trim();
  });

  return data;
}


// ─────────────────────────────────────────────────────────────────────────────
// updatePreview()
//
// Called on every input event and after renderForm().
// Reads current form values, runs the active template's generate(),
// and writes the result to #preview-output.
//
// Defined here as a stub so this file is self-contained;
// app.js can override or extend it after loading this file.
// ─────────────────────────────────────────────────────────────────────────────
function updatePreview() {
  if (!activeTemplateKey) return;

  const template = TEMPLATES[activeTemplateKey];
  if (!template) return;

  const output  = template.generate(getFormData());
  const preview = document.getElementById("preview-output");
  if (!preview) return;

  preview.textContent = output;

  const today    = new Date().toISOString().split("T")[0];
  const filename = `${activeTemplateKey}_${today}.md`;
  const words    = output.trim().split(/\s+/).filter(Boolean).length;
  const lines    = output.split("\n").length;
  const sections = (output.match(/^## /gm) || []).length;

  // Preview bar
  const wc = document.getElementById("word-count");
  if (wc) wc.textContent = `${words.toLocaleString()} words`;

  const pfn = document.getElementById("preview-filename");
  if (pfn) pfn.textContent = filename;

  // Stats bar
  const statsBar = document.getElementById("stats-bar");
  if (statsBar) statsBar.dataset.state = "loaded";

  const elWords    = document.getElementById("stat-words");
  const elLines    = document.getElementById("stat-lines");
  const elSections = document.getElementById("stat-sections");
  const elFile     = document.getElementById("stat-filename");

  if (elWords)    elWords.textContent    = words.toLocaleString();
  if (elLines)    elLines.textContent    = lines.toLocaleString();
  if (elSections) elSections.textContent = sections;
  if (elFile)     elFile.textContent     = filename;

  // Mark preview panel as loaded (triggers amber border via CSS)
  const panel = document.getElementById("preview-panel");
  if (panel) panel.dataset.state = "loaded";
}
