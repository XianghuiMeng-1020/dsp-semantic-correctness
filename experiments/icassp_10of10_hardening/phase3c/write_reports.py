"""Write Phase-3C reports from frozen JSON. Protocol lock is not overwritten."""
from __future__ import annotations

import json

from experiments.icassp_10of10_hardening.phase3c.config import OUT_DIR, REPORT_DIR


def _yn(v) -> str:
    if v is True:
        return "YES"
    if v is False:
        return "NO"
    return str(v)


def _load() -> dict:
    names = (
        "inventory",
        "leakage",
        "frozen_base_catalogs",
        "transfer",
        "maintenance",
        "secondary",
        "external_invalid",
        "dsp_mechanism",
        "novelty",
        "headline",
    )
    return {n: json.loads((OUT_DIR / f"{n}.json").read_text(encoding="utf-8")) for n in names}


def write_inventory(d: dict) -> None:
    inv = d["inventory"]
    lines = [
        "# PHASE 3C — Auxiliary corpus inventory",
        "",
        "Every listed corpus existed before Phase 3C. Eligibility requires catalog-exclusion from Phase-3B fitting, frozen task membership, independent certification, and non-duplicate coefficients.",
        "",
        "| corpus | existed pre-Phase3C | in base 412? | tasks mapped | independently certified? | used in Phase3B catalog selection? | eligible external holdout? |",
        "| ------ | ------------------- | ------------ | ------------ | ------------------------ | ---------------------------------- | -------------------------- |",
    ]
    for r in inv["corpora"]:
        tasks = r["tasks_mapped"]
        if isinstance(tasks, list):
            ttxt = f"{len(tasks)} tasks" if tasks else "none"
        else:
            ttxt = str(tasks)
        lines.append(
            f"| {r['corpus']} | {_yn(r['existed_pre_phase3c'])} | {_yn(r['in_base_412'])} | {ttxt} | "
            f"{_yn(r['independently_certified'])} | {_yn(r['used_in_phase3b_catalog_selection'])} | "
            f"{_yn(r['eligible_external_holdout'])} |"
        )
    lines += [
        "",
        "## Type-I probe provenance",
        "",
        f"- Unique certified probes: {inv['probe_n']} (unique paths {inv['probe_unique']})",
        f"- Tasks covered: {inv['probe_task_coverage']} FIR tasks (no IIR probes)",
        f"- CID overlap with constructed 412: {inv['cid_overlap_constructed_probe']}",
        f"- Per-task counts: `{inv['probe_per_task']}`",
        "- Construction: `data/icassp_10of10/feasible_probe.json` rows with `genuine_same_order`, a stored `path`, and `independent_ok`.",
        "- These probes were **not** members of the manuscript 412 constructed valids.",
        "- They **were** members of Phase-3B $V_t$ via `load_frozen_universe()`.",
        "",
        "## Phase-3B catalog membership of probes",
        "",
        f"- Coefficient catalog members that are probe paths: "
        f"{inv['catalog_probe_stats']['probe_catalog_refs']} / {inv['catalog_probe_stats']['total_catalog_refs']}",
        f"- Tasks whose optimal coefficient catalog contains at least one probe: "
        f"{inv['catalog_probe_stats']['tasks_with_probe_reference']} / 16 FIR",
        "",
        "| task | Phase-3B n_valid | K* | probe IDs in catalog |",
        "| ---- | ---------------: | -: | -------------------: |",
    ]
    for t in inv["catalog_probe_stats"]["per_task"]:
        lines.append(
            f"| {t['task']} | {t['n_valid']} | {t['K_obs_star']} | {t['probe_in_catalog']} |"
        )
    lines += [
        "",
        "## Eligibility conclusion",
        "",
        f"- Primary holdout designation: none",
        f"- Blocker: `{inv['blocker']}`",
        f"- Reason: {inv['blocker_reason']}",
        f"- Eligible secondary corpora: {inv['eligible_secondary'] or 'NONE'}",
        f"- Extra disk npy after excluding the 412: {len(inv['extra_disk_valid_files'])} (the independent-INVALID firwin2 flips)",
        f"- Optional catalog-excluded invalids: {len(inv.get('label_flip_invalids') or [])} eligible={inv.get('optional_external_invalid_eligible')}",
        f"- Generated-witness records: {inv['generated_n']} ({inv['generated_independent_ok']} independent_ok); stored implementations: {inv['generated_impl_keys_present']}",
        "",
        "Language: the Type-I probes are previously frozen auxiliary Type-I valid realizations that were **included** in the primary catalog-fitting universe. They are not temporally prospective and not a catalog-excluded dataset.",
        "",
    ]
    (REPORT_DIR / "PHASE3C_AUXILIARY_CORPUS_INVENTORY.md").write_text("\n".join(lines), encoding="utf-8")


def write_leakage(d: dict) -> None:
    leak = d["leakage"]
    c = leak["checks"]
    e = leak["evidence"]
    lines = [
        "# PHASE 3C — Leakage audit",
        "",
        f"Corpus: `{leak['corpus']}`",
        "",
        f"Verdict: `{leak['verdict']}`",
        "",
        f"Blocker: `{leak['blocker']}`",
        "",
        "Primary transfer is valid only if the first five relevant leakage checks are clean.",
        "",
        "| question | answer |",
        "| -------- | ------ |",
        f"| Was it part of base V? | {_yn(c['part_of_base_V'])} |",
        f"| Was it part of base I? | {_yn(c['part_of_base_I'])} |",
        f"| Was it a candidate reference in Phase 3B? | {_yn(c['candidate_reference_in_phase3b'])} |",
        f"| Did its distances affect Phase-3B K*? | {_yn(c['distances_affected_phase3b_Kstar'])} |",
        f"| Did its labels affect threshold selection? | {_yn(c['labels_affected_threshold_selection'])} |",
        f"| Was any catalog changed after its score was observed? | {_yn(c['catalog_changed_after_holdout_score'])} |",
        f"| Is it coefficient-identical to any selected reference? | {_yn(c['coefficient_identical_to_selected_reference'])} |",
        f"| Is it response-identical to any selected reference? | {c['response_identical_to_selected_reference']} |",
        "",
        f"First five relevant checks clean: `{_yn(leak['first_five_relevant_checks_clean'])}`",
        "",
        "## Evidence",
        "",
        f"- Phase-3B $V_t$ includes probes: {e['phase3b_V_includes_probes']}",
        f"- Probe n: {e['probe_n']}; constructed n: {e['constructed_n']}",
        f"- Exact CID overlap constructed vs probes: {e['cid_overlap_constructed_probe']}",
        f"- Probe paths among coefficient catalog members: {e['probe_catalog_refs']} / {e['total_catalog_refs']}",
        f"- FIR tasks with at least one selected probe reference: {e['tasks_with_probe_reference']}",
        f"- {e['note']}",
        "",
        "Do not score this corpus as `H_TYPEI` external validity.",
        "",
    ]
    (REPORT_DIR / "PHASE3C_LEAKAGE_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")


def write_dsp(d: dict) -> None:
    m = d["dsp_mechanism"]
    lines = [
        "# PHASE 3C — DSP transfer mechanism",
        "",
        "No external-validity transfer was scored. Mechanism strata on a leaked in-sample corpus would not answer the Phase-3C question.",
        "",
        f"- Q1 filter-type concentration: {m['filter_type']}",
        f"- Q2 same-order: {m['same_order']}",
        f"- Q3 Type-I: {m['type_i']}",
        f"- Q4 loose vs tight: {m['loose_vs_tight']}",
        f"- Q5 rejected holdouts still S_t-certified: {m['rejected_still_certified']}",
        "",
        f"DSP-mechanism verdict: `{m['verdict']}`",
        "",
        m["note"],
        "",
        "Phase-3A reminder: an ambient coefficient center exists on 19/20 tasks and a response center on 20/20. That isolates later catalog questions to **realizable reference semantics**, not raw sphere impossibility. It is not evidence of external-validity transfer.",
        "",
    ]
    (REPORT_DIR / "PHASE3C_DSP_TRANSFER_MECHANISM.md").write_text("\n".join(lines), encoding="utf-8")


def write_secondary(d: dict) -> None:
    s = d["secondary"]
    inv = d["external_invalid"]
    lines = [
        "# PHASE 3C — Secondary holdouts",
        "",
        "NONE",
        "",
        f"- Eligible secondary corpora: {s['n_eligible']}",
        f"- Consistent with primary: {s['consistent_with_primary']}",
        "",
        s["note"],
        "",
        f"EXTERNAL_INVALID_TRANSFER = `{inv['EXTERNAL_INVALID_TRANSFER']}`",
        "",
        inv.get("reason", ""),
        "",
    ]
    if inv.get("rows"):
        lines += [
            "| id | task | d_min | tau_safe | false accept |",
            "| -- | ---- | ----: | -------: | ------------ |",
        ]
        for r in inv["rows"]:
            if not r.get("task_id"):
                continue
            lines.append(
                f"| `{r['id']}` | {r['task_id']} | {r.get('d_min_coeff')} | {r.get('tau_safe')} | {_yn(r.get('false_accept'))} |"
            )
        lines.append("")
    (REPORT_DIR / "PHASE3C_SECONDARY_HOLDOUTS.md").write_text("\n".join(lines), encoding="utf-8")


def write_prior_art(_d: dict) -> None:
    lines = [
        "# PHASE 3C — Prior art: transfer and conformance",
        "",
        "This audit does **not** re-litigate generic set-cover. The question is whether prior work already uses a minimum catalog of conforming reference implementations, selected on one certified universe, then audits transfer and maintenance when additional conforming DSP realizations are admitted.",
        "",
        "## Generic prototype transfer",
        "",
        "**KNOWN.**",
        "",
        "Condensed nearest neighbor (Hart 1968), edited neighbors (Wilson 1972), and the prototype-selection taxonomy (García et al., IEEE TPAMI 2012) already evaluate selected prototypes on held-out labeled samples. Train/test evaluation of prototypes is not novel.",
        "",
        "## Conformance-testing preference for specifications",
        "",
        "**KNOWN.**",
        "",
        "Software-engineering conformance testing compares implementations to a specification rather than to a single reference binary. Wikipedia's reference-implementation discussion and NIST-style conformance suites treat a reference as an interpretation aid, not as the definition of correctness. Independent reimplementation work (e.g. SPE11B specification-conformance studies) shows that tests sharing a code's reading of a specification cannot detect that shared misreading.",
        "",
        "## DSP / filter implementation verification",
        "",
        "Hardware DSP verification commonly uses a MATLAB/Simulink model as a **golden reference** and checks RTL bit/cycle accuracy (DVCon UVM+dpigen flows; HDL Coder reference RTL; HLS C-vs-MATLAB testbenches). That is the opposite scientific object: one golden realization, not a specification-oracle catalog-burden plus catalog-excluded transfer audit.",
        "",
        "## Close DSP work with the same external-validity reference-catalog audit",
        "",
        "**NO.**",
        "",
        "No DSP/filter paper was found that (i) selects a minimum catalog of specification-valid reference realizations on one frozen certified universe, (ii) freezes that catalog, then (iii) asks whether independently certified additional realizations excluded from selection are accepted, and (iv) measures how much the catalog must grow if they are admitted. Absence of evidence is a boundary, not a priority claim.",
        "",
        "## Defensible novelty boundary",
        "",
        "Generic prototype transfer and specification-based conformance are known. Close DSP hardware verification uses golden MATLAB references rather than specification-membership catalogs. Phase 3C does **not** convert that literature gap into a transfer result, because the intended Type-I holdout leaked into Phase-3B catalog selection. The remaining manuscript-specific object is still the finite-universe RCC / reference-hierarchy diagnostic, not a new algorithm and not an external-validity theorem.",
        "",
        "### Required conclusions",
        "",
        "| item | verdict |",
        "| ---- | ------- |",
        "| Generic prototype transfer | KNOWN |",
        "| Conformance-testing preference for specifications | KNOWN |",
        "| Close DSP work with the same external-validity reference-catalog audit | NO |",
        "| Defensible novelty boundary | PARTIAL |",
        "",
    ]
    (REPORT_DIR / "PHASE3C_PRIOR_ART_TRANSFER.md").write_text("\n".join(lines), encoding="utf-8")


def write_redteam(d: dict) -> None:
    nov = d["novelty"]
    a = nov["attacks"]
    lines = [
        "# PHASE 3C — Novelty red team, round 3",
        "",
        "Attack the strongest possible Phase-3C story. Do not recommend new science merely to chase perfection.",
        "",
        "## C1. This is still finite.",
        "",
        "- Severity before Phase 3C: HIGH / OPEN (Phase-3B residual).",
        "- Actual evidence: the only large certified-valid auxiliary corpus (1260 Type-I probes) was inside Phase-3B $V_t$. No catalog-excluded holdout was scored.",
        f"- Residual severity: HIGH / `{a['C1_still_finite']}`.",
        "- Manuscript-safe defense: state that $K^*$ is a finite confirmatory-universe diagnostic.",
        "- Another experiment necessary? Only if the PI wants a **new** catalog-excluded corpus. That would be new science, not Phase 3C.",
        "",
        "## C2. This is just test-set evaluation of prototypes.",
        "",
        "- Severity before: HIGH.",
        "- Actual evidence: no clean test-set evaluation was performed. Claiming one would be false.",
        f"- Residual: `{a['C2_just_prototype_testset']}`. The attack is defused only by not claiming holdout transfer.",
        "- Manuscript-safe defense: do not describe Type-I probes as a test set for Phase-3B catalogs.",
        "- New experiment? Not required to avoid a false claim.",
        "",
        "## C3. The Type-I probes may be too similar to the base FIRs.",
        "",
        "- Severity before: MEDIUM.",
        "- Actual evidence: 467/825 selected coefficient references are probe paths, so probes were diverse enough to be chosen as covering realizations. That is an in-sample diversity fact, not external transfer.",
        f"- Residual: `{a['C3_typei_too_similar']}`.",
        "- Manuscript-safe defense: call them same-order Type-I confirmatory occupants, not an independent population sample.",
        "- New experiment? Not required for honesty.",
        "",
        "## C4. The holdout is only FIR.",
        "",
        "- Severity before: MEDIUM.",
        "- Actual evidence: there is no eligible holdout at all. IIR has no Type-I probe corpus.",
        f"- Residual: `{a['C4_holdout_only_fir']}` (and stronger: no holdout).",
        "- Manuscript-safe defense: do not claim IIR transfer.",
        "- New experiment? Only if the PI later authorizes a new IIR auxiliary corpus.",
        "",
        "## C5. Specification checking wins by definition because $S_t$ defines the labels.",
        "",
        "- Severity before: MEDIUM.",
        "- Actual evidence: labels were already specification-defined. Phase 3C did not create a new predicate.",
        f"- Residual: `{a['C5_st_wins_by_definition']}`.",
        "- Manuscript-safe defense: the paper compares oracles on a frozen predicate; it does not rediscover that specifications define compliance.",
        "- New experiment? No.",
        "",
        "## C6. Catalog maintenance is merely another set-cover computation.",
        "",
        "- Severity before: MEDIUM.",
        "- Actual evidence: expanded $K^*$ was not run, because admitting leaked probes does not expand the universe.",
        f"- Residual: `{a['C6_maintenance_is_setcover']}`.",
        "- Manuscript-safe defense: do not claim a maintenance-burden experiment.",
        "- New experiment? Not in Phase 3C.",
        "",
        "## C7. This still does not justify saying reference matching is bad in general.",
        "",
        "- Severity before: HIGH if overclaimed.",
        "- Actual evidence: Phase 3A ambient centers exist on 19/20 coefficient and 20/20 response tasks. Phase 3C adds no general impossibility.",
        f"- Residual: `{a['C7_not_all_reference_matching']}`.",
        "- Manuscript-safe defense: keep the claim inside this oracle family, these metrics, and this frozen universe.",
        "- New experiment? No.",
        "",
        "## C8. This belongs in software testing rather than ICASSP.",
        "",
        "- Severity before: MEDIUM.",
        "- Actual evidence: the objects remain FIR/IIR mask specifications and realization catalogs. The missing transfer result weakens, but does not erase, the DSP setting.",
        f"- Residual: `{a['C8_not_dsp']}`.",
        "- Manuscript-safe defense: lead with specification-defined filter correctness and reference-hierarchy diagnostics, not generic software testing.",
        "- New experiment? No.",
        "",
        "## DSP-specific mechanism question",
        "",
        "What would make this more than generic prototype selection is multiple DSP realizations satisfying the same frequency-domain specification, with catalogs encoding realization choice rather than only compliance, plus transfer/maintenance under additional certified realizations. Phase 3C **did not obtain** that last clause. The DSP content that remains is the Phase-1/3A/3B hierarchy on frozen FIR/IIR masks, not a transfer theorem.",
        "",
        f"NOVELTY_10OF10_GATE: `{nov['NOVELTY_10OF10_GATE']}`",
        "",
        f"Internal novelty score: {nov['internal_novelty']}",
        "",
        f"Best framing: {nov['best_framing']}",
        "",
        nov["strongest_novelty"],
        "",
    ]
    (REPORT_DIR / "PHASE3C_NOVELTY_REDTEAM.md").write_text("\n".join(lines), encoding="utf-8")


def write_all_reports() -> None:
    d = _load()
    write_inventory(d)
    write_leakage(d)
    write_dsp(d)
    write_secondary(d)
    write_prior_art(d)
    write_redteam(d)
