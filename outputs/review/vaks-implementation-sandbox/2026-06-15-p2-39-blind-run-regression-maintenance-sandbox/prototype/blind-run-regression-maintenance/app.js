const decisions = [
  { run: "blind_read_only_recovery", decision: "inspect_only" },
  { run: "blind_formal_vault_boundary_stop", decision: "stop_and_ask_user_if_boundary_crossing_is_needed" },
  { run: "blind_fresh_sandbox_continuation", decision: "start_new_sandbox_only" }
];

const grid = document.getElementById("decision-grid");

for (const item of decisions) {
  const card = document.createElement("article");
  card.className = "card";
  card.innerHTML = `<strong>${item.run}</strong><span>${item.decision}</span>`;
  grid.appendChild(card);
}
