# CCR-2 reel series: research and staging notes

Research date: 2026-09-16. Production source: `notes/worked/symmetry-ccr-2.md`.

The adaptation is a cumulative, silent series. Each 30–60 second reel should establish one visual relationship, then leave the next reel a concrete question. Explanatory captions accompany the posts; the animations still need enough labels to be intelligible without opening the caption. Account configuration and publishing can wait until the entire series is staged.

## Comparable short-form work

These are actual short-form examples or a creator's explicitly portrait-format source, not long-form videos relabeled as reels. No external footage, music, or code has been copied into the production.

| Reference | Evidence inspected | Useful lesson for this series |
| --- | --- | --- |
| 3Blue1Brown, [The topology of two-note chords](https://www.youtube.com/shorts/K-pGGb0f3tc) | Creator's YouTube Short; primary channel attribution; sampled frames during playback. The portrait composition places a note circle above a piano keyboard and matches highlighted notes across them. | Two views can explain each other without competing. Carry a color from the mathematical object to its other representation. Our path/phasor and packet/modes pairs should use precisely this kind of correspondence. |
| 3Blue1Brown, [How word vectors encode meaning](https://www.youtube.com/shorts/FJtFZwbvkI4) | Creator's YouTube Short; primary channel attribution; opening and playback frames. A pair of stacked vector diagrams uses color consistently between labels, vectors, and equations. | Give equations their own room; use repeated visual structure for an analogy. Our x and k views should receive the same treatment. Avoid letting subtitles cross the geometry: the silent version can use a separate short-label band. |
| 3Blue1Brown, [A short on shorts](https://www.youtube.com/watch?v=TaopSi3Ucfc) | Creator's title and description explicitly identify the short format and link its animations to longer treatments of fractals. This item was located, not fully watched. | A short can be an entry into a larger argument. Include episode numbering and a clear route to the full chapter, without pretending every reel proves its conclusion alone. |
| Jhagas Hana Winaya, [FourierVideoReels source](https://gist.github.com/jhagas/201886612a49c833bfdfb566babd60e4) | Creator-published code explicitly renders 1080×1920. It updates a partial-sum graph and its equation together for 19 terms; pauses between updates are 0.3 seconds after an initial 0.5-second hold. | A changing equation should be tied to the changing picture. Progressive addition is already an effective short-form idiom. Those timings are evidence about this example, not a requirement for our denser subject. |

The creator's [account of adapting longer work into shorts](https://members.3blue1brown.com/posts/shorts-82511260) confirms the adaptation strategy. Our series differs in being a connected argument with silent animation and an explanatory post caption. It should not depend on remembered narration from a longer video.

The directly inspected comparison set is small and strongest on mathematical visualization. It is not an exhaustive Instagram survey or evidence about algorithmic performance. No engagement, retention, or optimal-posting claims follow from it.

## Decisions supported by this research

- Compose for the portrait canvas instead of shrinking a landscape lecture figure.
- Put a meaningful transformation in the first two seconds. Do not reserve most of the motion for the ending.
- Keep one principal equation on screen; reveal or transform the terms in step with the geometry.
- Keep object colors stable across related views and across episodes. Color must identify the same mathematical contribution, not just decorate it.
- Use short changing labels to replace what narration would otherwise supply. Keep the fuller argument in the post caption.
- Number the sequence visibly. Finish each caption with the next conceptual step, not a generic engagement prompt.
- Use the existing manuscript assets as mathematical and aesthetic references. Render phone-sized labels afresh.

These are production judgments informed by the examples, not claims that a particular format guarantees an audience.

## Thirteen-episode coverage and caption emphasis

| No. | Claim the viewer should leave with | Caption emphasis / mathematical guardrail |
| --- | --- | --- |
| 01 | A wave function can be translated in position or wave number. | Show both in their own representation with symmetric visual treatment. A k translation in position representation multiplies by exp(ibx); it does not merely move the position envelope. |
| 02 | Applying the same translation to two functions preserves their overlap. | Unitarity concerns the complex inner product. A drawn angle/projection is a schematic real-overlap example. Label it as such without making the episode an apology for the simplification. |
| 03 | Global phase turns a complex function while leaving its magnitude fixed. | Each mode receives the same phase, not the same spatial displacement. The sum must be the actual sum of the displayed modes. A pure mode alone cannot visually distinguish a phase shift from a matching position shift. |
| 04 | An x–k loop closes in its two translation coordinates but leaves a phase. | For chronological +k, +x, −k, −x, the residual is exp(−iab). The operator product acts from right to left. [X,K]=iI and the central commutators close the algebra generated here. H₃ is a compact name for this structure. |
| 05 | Localization trades position spread against wave-number spread. | Use normalized Fourier partners. Define σ from squared magnitude and label the pictured Gaussian family as saturating σxσk=1/2; do not imply every envelope is Gaussian. |
| 06 | Propagation advances phase, and short wavelengths can give narrow transmitted beams. | A mode is exp[i(kx−ωt)]. If crests become too fine to draw, explicitly switch to cycle-averaged intensity. A change in rendering is not itself the mathematical limit. |
| 07 | Along a route, phase factors multiply; across routes, amplitudes add. | The A→C→B and A→D→B geometry must supply the same lengths and weights used by the two complex arrows. Intensity is the square of the resultant magnitude. |
| 08 | The same addition works for many contributions. | The path pane, tip-to-tail chain, and detector pattern must use the same numerical model. Finite slit contributions include the integration across each slit. Route drawings identify contributions rather than tracked particle histories. |
| 09 | Dense intermediate wavelet constructions recover free propagation. | The incoming plane wave is deliberate. Distinguish schematic component arcs from their coherent sum. Recovering unobstructed space requires the opaque parts to disappear; adding opaque barriers indefinitely would describe another experiment. Use a correctly normalized propagation law. |
| 10 | Short wavelength makes nonstationary contributions cancel across increasingly small path variations. | Phase remainders are deterministic. Fixed finite samples eventually underresolve the winding, so resolve the shortest wavelength. Use matched path/phasor colors to make the narrow stationary region visible; do not force the curve to straighten or discard real contributions. |
| 11 | Quantum mechanics gives the wave calculation a measurement interpretation. | The Born rule is a physical input: normalized squared magnitude gives measurement probabilities. A sum over candidate histories is a calculation; it does not by itself assert that a particle literally traverses each drawn route. Show accumulated detections, not a fake selection of one hidden drawn path. |
| 12 | Spacetime geometry and experiment connect phase to mechanical action. | This is the chapter's compact bridge to the next chapter, not a complete derivation. Introduce mass as the invariant labeling a mass shell. For the free proper-time comparison use c=1 explicitly: S=−mτ, φ=−κτ, m/κ=ħ. A universal measured calibration supplies ħ; the abstract commutator does not determine it. |
| 13 | The same scale turns wave number into momentum and Fourier uncertainty into quantum uncertainty. | P=ħK, [X,P]=iħI, σxσp≥ħ/2. A particular law of time evolution additionally needs a Hamiltonian or the corresponding dynamical input. The series has connected the structures; it has not derived every interaction from the CCR alone. |

For the final three captions, a useful compact bridge is: “So far, this has been wave mathematics. Quantum mechanics supplies a physical interpretation for its squared magnitude. Spacetime structure and a measured scale then connect its phase to action, and its wave number to momentum.” Keep this distinction clear without repeatedly interrupting the story with disclaimers.

## Publishing feasibility

Meta's own [Instagram Reels publishing sample](https://github.com/fbsamples/reels_publishing_apis/blob/main/insta_reels_publishing_api_sample/README.md) confirms a programmable workflow: create a media container, supply or upload the video, wait for processing, then publish. It supports a cover image URL or a thumbnail timestamp, plus a resumable upload path for a local video. Its recommended portrait ratio is 9:16, with MP4/H.264 among the supported formats. The sample describes a Facebook-login setup, so it should not be treated as the only current account-connection route. Its fixed account-limit numbers can become stale; a publisher should query the account's publishing limit rather than assume a quota.

The current direct [content-publishing documentation](https://developers.facebook.com/docs/instagram-platform/content-publishing) and [media reference](https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-user/media) could not be fetched in this research session. Recheck current account eligibility, permission names, media limits, and API version when configuring the actual publishing account. No Postman page was opened during this task, and no publishing software or account connection was installed.

Practical staging format, chosen conservatively:

- 1080×1920, 24 fps, progressive H.264, yuv420p, MP4 with fast-start metadata.
- Silent track policy: omit audio for now. If an eventual uploader insists on a track, add silent AAC during that adapter's export without changing the picture.
- Aim below 100 MB per reel; the requested durations do not need an aggressive bitrate.
- Caption in a separate UTF-8 text file. Instagram post text is plain text, so equations in captions use readable Unicode rather than unrendered LaTeX.
- Separate portrait cover, with an explicit video-frame fallback recorded in the manifest.
- Ordered manifest: episode number, title, duration, local video path, local cover path, caption path, thumbnail timestamp, source section, publication state, and optional future schedule.
- Keep `publication_state` staged until account setup and publishing are requested. Record returned container/post IDs when publishing later so retries do not create duplicate posts.

“Batch ready” here means all finished assets and their metadata can be fed into one later queue. It does not mean thirteen posts should go live simultaneously. A cumulative series benefits from an explicit order, which the package can preserve regardless of the eventual schedule. No accounts, tokens, hosting, or publishing decisions are needed to finish the local package.

The API sample demonstrates that batch automation is technically feasible. A working live publisher still requires the eventual account's authorization and a current API validation pass. No claim is made that Meta Business Suite provides a universal CSV-import workflow.
