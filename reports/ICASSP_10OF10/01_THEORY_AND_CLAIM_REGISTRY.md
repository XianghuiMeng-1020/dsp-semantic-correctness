# 01 — Theory and claim registry

**Status:** written before manuscript insertion.  
**Thesis:** When can a reference-based evaluation oracle be a *correct* oracle for a specification-defined DSP task?

This document is the only authorized source of formal language for the strengthening pass. The manuscript must not later upgrade any empirical statement into a global theorem.

---

## 1. Objects

Fix a specification/task \(t\) and an explicitly stated **evaluation universe** \(\mathcal{U}_t\) (the independently verified candidate set used for that task in this study).

A **realization** is a concrete filter (or identity map) \(h\).

The **specification-valid set** is

\[
\mathcal{V}_t=\{h:S_t(h)=1\}.
\]

\(S_t\) is the specification predicate, not a distance to any library design.

A **reference realization** \(h_r\) is one distinguished element that some evaluation protocol treats as canonical. It need not be unique in \(\mathcal{V}_t\).

Given a distance \(d\) and threshold \(\tau\), the **reference acceptance region** is

\[
\mathcal{A}_{\tau,r}=\{h:d(h,h_r)\le\tau\}.
\]

These three objects are distinct:

| Object | Meaning |
|---|---|
| Reference realization \(h_r\) | one point |
| Reference acceptance region \(\mathcal{A}_{\tau,r}\) | a ball (or sublevel set) around that point |
| Specification feasible set \(\mathcal{V}_t\) | all realizations meeting the contract |

A reference-based oracle declares “correct” iff \(h\in\mathcal{A}_{\tau,r}\).  
A specification-based oracle declares “correct” iff \(h\in\mathcal{V}_t\).

---

## 2. Soundness, completeness, exactness

Relative to \(\mathcal{V}_t\):

**Soundness**

\[
\mathcal{A}_{\tau,r}\subseteq\mathcal{V}_t.
\]

Every accepted reference-neighbor is specification-valid. Failure = false acceptance (invalids inside the ball).

**Completeness**

\[
\mathcal{V}_t\subseteq\mathcal{A}_{\tau,r}.
\]

Every specification-valid realization is accepted. Failure = false rejection (valids outside the ball).

**Exactness**

\[
\mathcal{A}_{\tau,r}=\mathcal{V}_t.
\]

The reference ball recovers the specification set exactly.

These are definitions about set inclusion. They are not claims that \(d\) is a DSP-optimal metric.

---

## 3. Finite-universe threshold criterion

Restrict attention to the evaluated universe \(\mathcal{U}_t\). Define

\[
D_V(r)=\sup_{h\in\mathcal{V}_t\cap\mathcal{U}_t}d(h,h_r)
\]

and

\[
D_I(r)=\inf_{h\in\mathcal{U}_t\setminus\mathcal{V}_t}d(h,h_r).
\]

If \(\mathcal{V}_t\cap\mathcal{U}_t=\emptyset\), \(D_V\) is undefined.  
If \(\mathcal{U}_t\setminus\mathcal{V}_t=\emptyset\), \(D_I\) is undefined.

**Finite-universe exact-threshold criterion (proved for finite \(\mathcal{U}_t\)).**  
A scalar threshold on \(d(\cdot,h_r)\) classifies every point of \(\mathcal{U}_t\) exactly (valid vs invalid) if and only if there exists \(\tau\) with

\[
D_V(r)\le\tau<D_I(r).
\]

**Proof.**  
(\(\Rightarrow\)) If some \(\tau\) classifies \(\mathcal{U}_t\) exactly, every valid has \(d\le\tau\) and every invalid has \(d>\tau\), so \(D_V\le\tau<D_I\).  
(\(\Leftarrow\)) If \(D_V\le\tau<D_I\), every evaluated valid is \(\le D_V\le\tau\) and every evaluated invalid is \(\ge D_I>\tau\).

**Corollary.** If \(D_V(r)\ge D_I(r)\), no scalar threshold on distance to that reference can perfectly recover specification membership on \(\mathcal{U}_t\).

This corollary is an **empirical / finite-set non-separability certificate on the evaluated universe**.  
It is **not** a theorem that no threshold works over the infinite set of all filters unless the extrema \(D_V,D_I\) are certified over that larger set.

---

## 4. Reference-separability gap

\[
G_r=D_I(r)-D_V(r).
\]

| Sign | Meaning on \(\mathcal{U}_t\) |
|---|---|
| \(G_r>0\) | a threshold interval exists; exact scalar separation is possible |
| \(G_r\le 0\) | no scalar threshold on this \(d(\cdot,h_r)\) separates all evaluated valids from all evaluated invalids |

An **ordering inversion witness** is a pair \((h_{\mathrm{valid}},h_{\mathrm{invalid}})\) in \(\mathcal{U}_t\) with

\[
S_t(h_{\mathrm{valid}})=1,\quad S_t(h_{\mathrm{invalid}})=0,\quad d(h_{\mathrm{invalid}},h_r)<d(h_{\mathrm{valid}},h_r).
\]

Existence of any such pair implies \(G_r\le 0\) for that \(d\) and \(r\).

Name used in this project: **reference-separability gap**.  
Not used: “impossibility theorem,” “no reference can ever work,” “the feasible set is non-convex so matching is impossible.”

---

## 5. Multi-reference balls

For a finite reference set \(\mathcal{R}_K\),

\[
d_K(h)=\min_{r\in\mathcal{R}_K}d(h,h_r),
\qquad
\mathcal{A}_{\tau,\mathcal{R}_K}=\{h:d_K(h)\le\tau\}.
\]

The same \(D_V,D_I,G\) diagnostics apply with \(d_K\) in place of \(d(\cdot,h_r)\).

Scientific question: does a finite library of canonical realizations recover \(\mathcal{V}_t\cap\mathcal{U}_t\), or does the mismatch persist?

---

## 6. Statement classes (mandatory separation)

### Formally proved (this document)

1. For a **finite** \(\mathcal{U}_t\), exact classification by one scalar threshold on \(d(\cdot,h_r)\) holds iff \(D_V(r)\le\tau<D_I(r)\) for some \(\tau\).
2. If \(D_V(r)\ge D_I(r)\) on that finite set, no such \(\tau\) exists.
3. Soundness / completeness / exactness are equivalent to the stated inclusions.

These proofs do not depend on FIR/IIR structure. They are evaluation-geometry facts.

### Finite-set empirical statements (allowed after experiments)

- On the independently verified candidate set of task \(t\), \(G_r\le 0\) (or \(>0\)) for a named distance and named reference.
- \(k\) of \(20\) Suite N tasks exhibit an inversion witness.
- Same-order Type-I probe found a valid reference-discordant alternative on \(k\) of \(16\) FIR tasks.
- Singleton suite is **effectively singleton over the evaluated representation/universe**.

### Numerical evidence (not theorems)

- Task-macro FRR and bootstrap CIs.
- Pooled occupant FRR (secondary).
- Threshold-sweep best balanced accuracy.
- Generated-code existence witness.

### Hypotheses (not to be written as results)

- Near-boundary invalids are systematically closer to \(h_r\) than some valids.
- Response-space distance separates when coefficient distance does not (or the reverse).
- Some other untested canonical designer family would restore exactness.

### Manuscript-safe claims (only if later experiments support them)

- A reference-distance oracle answers “near this realization?” not “in \(\mathcal{V}_t\)?”
- On the evaluated universe, a scalar threshold on distance to a named reference is exact iff the reference-separability gap is positive.
- When \(G_r\le 0\), no post-hoc threshold choice on that distance/reference pair can remove both FRR and FAR on that universe.
- Same-order / same-structure valid alternatives, if found and independently verified, show that disagreement is not explained only by order change, zero-padding, or trivial re-encoding.
- Suite S is a **positive control**: when the specification is effectively singleton in the evaluation representation, reference matching and \(S_t\) can agree.

### Forbidden overclaims

- “It is impossible for any reference-based test to evaluate filter specifications.”
- “We prove non-uniqueness of optimal FIR/IIR filters” (classical and obvious).
- “4096- or 131072-point sampling certifies the continuous mask.”
- “Oracle C / the independent verifier is an external gold standard for all DSP implementations.”
- “\(\tau_R=0.05\) is the scientifically distinguished threshold.”
- “374/416 is a rate over real-world or generated DSP code.”
- “20 tasks represent DSP evaluation in general.”
- “Adding \(K\) library references recovers the feasible set” without the \(K\)-sweep.
- “The specification identifies a unique filter” when only the evaluated universe was searched.
- “Coefficient matching is what the community exclusively does” as an uncited sociological claim.
- Any claim that labels were preserved because the old headline was convenient.

---

## 7. What the paper is *not*

- Not a new FIR/IIR design algorithm.
- Not an LLM / generated-code leaderboard.
- Not a software-verification completeness theorem.
- Not a claim that Parks–McClellan / Remez / Butterworth are incorrect designers.
- Not a claim that specification masks are the only legitimate notion of correctness.

The paper asks a **correctness-oracle** question about DSP evaluation.

---

## 8. Positive-control role of Suite S

If a specification is **effectively singleton** on \(\mathcal{U}_t\) in the chosen representation, then \(D_V(r)\) is the distance from \(h_r\) to the (near-)unique valid class and \(G_r>0\) is expected whenever invalids are representably different.

Language required: “effectively singleton over the evaluated representation/universe,” not “mathematically unique among all functions,” unless a uniqueness proof is given.

---

## 9. Independent verification vs construction checking

Construction/`search_checker` may be approximate and may generate candidates.  
Final \(\mathcal{U}_t\) membership and all manuscript labels must come from an **independent** verifier that does not call the construction checker.

Dense sampling plus local extremum refinement is still a **numerical certificate**, not a continuous-frequency proof.
