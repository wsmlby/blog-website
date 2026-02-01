---
title: "How Reliable Are Consumer PC Components? A Data-Driven Analysis"
date: "2026-02-01"
author: "wsmlby with Claude"
summary: "If you built 1,000 PCs with consumer parts, how many would still be working perfectly after 30 days? After 3 years? We dig into publicly available failure rate data to find out."
---

# If You Built 1,000 PCs, How Many Would Survive?

Building a PC is a rite of passage for many enthusiasts. But every builder has faced the same anxiety: *will it POST?* And more importantly — will it still be running fine a year from now? Three years from now?

This post attempts to answer a deceptively simple question: **if you assembled 1,000 identical consumer PCs today, how many would be running perfectly after 30 days, and how many after 3 years?** We'll use publicly available failure rate data from system builders, retailers, and cloud storage providers to build a probabilistic model.

## The Bathtub Curve: Why Timing Matters

Before diving into numbers, it's important to understand the **bathtub curve** — the standard reliability model for electronic components <a href="https://en.wikipedia.org/wiki/Bathtub_curve">[1]</a>. Failure rates follow three phases:

1. **Infant Mortality (first weeks to months):** High but rapidly decreasing failure rate. Manufacturing defects, shipping damage, and weak components reveal themselves early. Industry practice considers the first 30–90 days as this window <a href="https://en.wikipedia.org/wiki/Bathtub_curve">[1]</a><a href="https://www.itl.nist.gov/div898/handbook/apr/section1/apr124.htm">[2]</a>.
2. **Useful Life (months to years):** A low, roughly constant failure rate driven by random events — power surges, thermal stress, cosmic rays flipping bits.
3. **Wear-Out (years):** Increasing failure rate as components physically degrade. Electrolytic capacitors dry out, NAND flash cells wear, and mechanical parts (fans, HDDs) accumulate fatigue.

<svg id="bathtubCurveChart" class="my-8"></svg>
<p class="text-center text-sm text-gray-600 -mt-4">
    The classic "bathtub curve": failure rate is highest at the start (infant mortality), drops to a low constant rate during useful life, then rises again as components wear out.
</p>

The practical implication: a component that survives its first month will very likely survive for years. As one repair technician put it: "If your board survives the first month, it'll probably last 10 years" <a href="https://forums.tomshardware.com/threads/chances-of-getting-a-doa-mobo.621254/">[3]</a>.

## Data Sources

We draw from the following public datasets:

| Source | Description | Time Span |
|---|---|---|
| **Puget Systems** <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a><a href="https://www.pugetsystems.com/labs/articles/most-reliable-pc-hardware-of-2021-2279/">[5]</a> | US workstation builder; tracks failure rates across all components with >200-unit minimums. Separates "shop" (testing/assembly) failures from "field" (customer) failures. | 2015–2024 |
| **Digitec Galaxus** <a href="https://hothardware.com/news/gpu-mb-failure-rates-digitec-galaxus">[6]</a> | Largest Swiss electronics retailer; publishes warranty return rates by brand for products with >300 units sold over 2 years. | 2021–2023 |
| **Hardware Sugar** <a href="https://www.tomshardware.com/news/retailer-shares-failure-rates-for-gpus-motherboards-ssds-more">[7]</a> | Philippines retailer; published RMA data over 4 years of operation. | 2020–2024 |
| **Backblaze** <a href="https://www.backblaze.com/blog/backblaze-drive-stats-for-2024/">[8]</a><a href="https://www.backblaze.com/blog/ssd-edition-2023-mid-year-drive-stats-review/">[9]</a> | Cloud storage company; publishes quarterly and annual drive failure statistics for ~300,000 drives. | 2013–2025 |
| **Mindfactory** <a href="https://www.pcworld.com/article/394099/ryzen-5000-failure-rates-we-reality-check-the-claims.html">[10]</a> | German retailer; RMA data for AMD Ryzen 5000 series CPUs. | 2020–2021 |

## Per-Component Failure Rates

The following chart summarizes our estimated 3-year failure rates for each component category, derived from the sources above:

<svg id="failureRateChart" class="my-8"></svg>
<p class="text-center text-sm text-gray-600 -mt-4">
    <strong>Note:</strong> Rates represent estimated 3-year cumulative failure probability for a typical consumer-grade component. RAM rate is for 2 sticks combined. HDD included for reference (many builds are SSD-only).
</p>

### CPU — Estimated 3-Year Failure Rate: 2.5%

CPUs have become surprisingly unreliable in recent years — not because silicon has gotten worse, but because modern CPUs now integrate memory controllers, PCIe controllers, and are pushed to aggressive power and thermal limits.

Puget Systems reports an overall CPU failure rate of **~5%** in 2024 (shop + field combined), with roughly half caught during assembly/testing and half failing in the field <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a>. This ~5% average has been the norm for the last few years. Retailer Mindfactory's RMA data for AMD Ryzen 5000 series showed lower rates of 0.37%–0.77%, though retailer RMA data only captures failures that customers bother to return <a href="https://www.pcworld.com/article/394099/ryzen-5000-failure-rates-we-reality-check-the-claims.html">[10]</a>.

**The 2024 Intel crisis deserves special mention.** Intel's 13th and 14th Gen desktop CPUs suffered from a microcode bug causing elevated voltages (a "Vmin shift"), leading to permanent silicon degradation. Intel confirmed damage was irreversible even after BIOS patches <a href="https://www.xda-developers.com/worst-pc-hardware-failures-2024/">[11]</a>. Puget Systems avoided the worst of it by using conservative BIOS power settings since 2017, keeping their Intel 13th/14th Gen failure rate at ~2% — far below what enthusiast builders using default motherboard settings likely experienced <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a>.

**For our model:** We use **2.5%**, representing the field-only portion of Puget's ~5% total. The "shop" failures don't apply to self-builders but do indicate that ~2.5% of CPUs will fail during initial setup or early use.

### GPU (Graphics Card) — Estimated 3-Year Failure Rate: 2%

GPUs consistently rank among the higher-failure-rate components, driven by high power draw, complex cooling, and heavy thermal cycling.

Digitec Galaxus, the largest Swiss electronics retailer, published warranty return data across all GPU brands over a 2-year period. The rates ranged from 0.4% to 2.5%, with a cross-brand average of approximately **1.5%** over 2 years <a href="https://hothardware.com/news/gpu-mb-failure-rates-digitec-galaxus">[6]</a>. Hardware Sugar, a Philippines retailer tracking 4 years of RMA data, reported GPU failure rates of 1.5%–5% depending on brand <a href="https://www.tomshardware.com/news/retailer-shares-failure-rates-for-gpus-motherboards-ssds-more">[7]</a>. Puget Systems notes that NVIDIA's professional Ada-generation GPUs had the lowest failure rates of any GPU generation they've sold <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a>.

**For our model:** We use **2%** as a 3-year estimate, extrapolating from the ~1.5% average over Digitec's 2-year window.

### Motherboard — Estimated 3-Year Failure Rate: 4%

Motherboards are complex PCBs with hundreds of solder joints, voltage regulators, and connectors. They consistently show one of the highest failure rates of any component.

Puget Systems reports an average motherboard failure rate of **4.9%** in 2024, and historically **~5.5%** (1 in 18) during 2015–2016 <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a><a href="https://www.pugetsystems.com/labs/articles/most-reliable-pc-hardware-of-2021-2279/">[5]</a>. Digitec Galaxus warranty data shows a range of 2.8%–5% across brands over 2 years <a href="https://hothardware.com/news/gpu-mb-failure-rates-digitec-galaxus">[6]</a>.

**For our model:** We use **4%**, slightly below Puget's 4.9% average since their figure includes shop failures that a self-builder would catch at setup.

### RAM (Memory) — Estimated 3-Year Failure Rate: 0.5% per stick

RAM has become remarkably reliable, especially when running at JEDEC-standard speeds (i.e., not overclocked XMP profiles).

Puget Systems reports an overall RAM failure rate of **~0.5%** in 2024, with only **0.16%** (1 in 625) failing in the field <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a>. Historical data shows ECC/Registered DDR4 at an even lower 0.2% total (0.04% field) <a href="https://www.pugetsystems.com/labs/articles/most-reliable-pc-hardware-of-2021-2279/">[5]</a>.

**For our model:** We use **0.5% per stick** (1.0% combined for 2 sticks) as a 3-year failure rate for consumer non-ECC RAM.

### Storage: SSD (NVMe / SATA) — Estimated 3-Year Failure Rate: 1%

Modern NVMe SSDs are among the most reliable components in a system.

Puget Systems reports an overall NVMe SSD failure rate of just **0.08%** (1 in 1,250) for their most-used drives in 2024, with only a single drive failing in the field <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a>. Backblaze's SSD boot drive fleet (3,300+ SSDs) shows a lifetime annualized failure rate (AFR) of **0.90%** as of mid-2023 <a href="https://www.backblaze.com/blog/ssd-edition-2023-mid-year-drive-stats-review/">[9]</a>.

**For our model:** We use **1%** as a conservative 3-year estimate, aligning with Backblaze's fleet-wide AFR (which represents heavier usage than a typical desktop).

### Storage: HDD — Estimated 3-Year Failure Rate: 4%

If your build includes a mechanical hard drive (for bulk storage), the numbers are well-documented thanks to Backblaze's fleet of ~300,000 drives.

The 2024 fleet-wide AFR was **1.57%**, and the lifetime AFR across all drives stands at **1.31%** <a href="https://www.backblaze.com/blog/backblaze-drive-stats-for-2024/">[8]</a>. Failure rates noticeably increase as drives exceed 5 years of service. A 1.31% annual rate compounds to roughly 3.9% cumulative failure probability over 3 years.

**For our model:** We use **4%** as a 3-year HDD failure rate. If your build is SSD-only, you can skip this.

### Power Supply (PSU) — Estimated 3-Year Failure Rate: 1.5%

PSU reliability data is scarce because manufacturers report MTBF (typically 300,000–500,000 hours) rather than real-world failure rates.

Puget Systems reports a **0.26%** total failure rate for their PSUs in 2024, with less than 0.1% failing in the field <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a>. Hardware Sugar's 4-year RMA data shows rates ranging from <1% to 2% across brands <a href="https://www.tomshardware.com/news/retailer-shares-failure-rates-for-gpus-motherboards-ssds-more">[7]</a>. A theoretical PSU with a 500,000-hour MTBF running 24/7 for 3 years has a ~5% failure probability, though real-world desktop usage (8–12 hours/day) would be considerably lower <a href="https://flexpowermodules.com/resources/fpm-designnote002-power-supply-reliability-aspects">[12]</a>.

**For our model:** We use **1.5%** as a 3-year failure rate for a quality consumer PSU (80+ Gold or better).

### Network Interface Card (NIC) / Onboard Ethernet — Estimated 3-Year Failure Rate: 1%

NIC reliability data is the hardest to find — manufacturers don't publish it, and since most NICs are integrated into the motherboard, failures often get lumped into motherboard RMA statistics.

Pre-owned hardware vendor CXtec reports a >99.5% reliability rating for network hardware (<0.5% failure), while some OEMs report failure rates in the 3–4% range <a href="https://www.cxtec.com/blog/network-hardware-failures-shocking-truth/">[16]</a>. Onboard NIC failure is a recognized failure mode, with certain controller families more prone than others <a href="https://forum.netgate.com/topic/100700/onboard-intel-or-external-nic">[13]</a>.

Notably, Intel's 2.5GbE controllers (I225-V and I226-V), shipped on most Z690/Z790/B760 motherboards, have a **known design flaw** causing intermittent connection drops <a href="https://hardforum.com/threads/intel-1226-v-2-5gbe-ethernet-chipset-showing-connection-drop-issues-chipset-used-on-most-raptor-lake-motherboards.2025009/">[14]</a><a href="https://www.tomshardware.com/news/intel-patches-stuttering-ethernet-issues-but-its-just-a-workaround-for-now">[15]</a>. Intel has released driver workarounds but no full hardware fix as of 2025. Builds using these controllers should expect a higher rate of *functional* issues (connection drops), even if the hardware doesn't fully die.

**For our model:** We add a separate **1%** failure rate for NIC-specific issues (driver/firmware bugs, controller defects not caught by motherboard-level testing) over 3 years.

### Cooling (Fans, AIO Coolers) — Estimated 3-Year Failure Rate: 1.5%

Hardware Sugar's 4-year RMA data shows cooling failure rates ranging from 0% to 4% depending on brand <a href="https://www.tomshardware.com/news/retailer-shares-failure-rates-for-gpus-motherboards-ssds-more">[7]</a>. AIO (All-in-One) liquid coolers add a pump and fluid loop as failure points, while air coolers with a single fan are essentially indestructible.

**For our model:** We use **1.5%** for a typical cooler (blended air/AIO) over 3 years.

## The Model: 1,000 PCs

We'll model a typical consumer gaming/workstation PC:

- 1x CPU
- 1x GPU
- 1x Motherboard
- 2x RAM sticks
- 1x NVMe SSD
- 1x PSU
- 1x Cooler
- 1x NIC (onboard, counted separately from mobo)

We assume component failures are independent (a simplification — in reality, a PSU failure can take out other components).

### 30-Day Survival (Infant Mortality)

Industry data suggests that roughly **40–60% of all lifetime failures occur in the first 30 days** (the infant mortality period) <a href="https://en.wikipedia.org/wiki/Bathtub_curve">[1]</a><a href="https://www.itl.nist.gov/div898/handbook/apr/section1/apr124.htm">[2]</a>. Puget Systems data confirms this: approximately half of their total failures are caught during assembly and initial testing <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">[4]</a>. For a self-builder, these manifest as DOA parts or failures during the first week of use.

We estimate 30-day failure rates as **~50% of the 3-year failure rate** for each component (front-loading failures per the bathtub curve):

| Component | 3-Year Failure Rate | Est. 30-Day Failure Rate |
|---|---|---|
| CPU | 2.5% | 1.25% |
| GPU | 2.0% | 1.0% |
| Motherboard | 4.0% | 2.0% |
| RAM (x2 sticks) | 0.5% per stick → 1.0% combined | 0.5% |
| NVMe SSD | 1.0% | 0.5% |
| PSU | 1.5% | 0.75% |
| Cooler | 1.5% | 0.75% |
| NIC (onboard) | 1.0% | 0.5% |

**P(all components survive 30 days)** = (1 - 0.0125) × (1 - 0.01) × (1 - 0.02) × (1 - 0.005)² × (1 - 0.005) × (1 - 0.0075) × (1 - 0.0075) × (1 - 0.005)

**= 0.9875 × 0.99 × 0.98 × 0.995² × 0.995 × 0.9925 × 0.9925 × 0.995**

**≈ 0.932**

### 30-Day Result: ~932 out of 1,000 PCs working perfectly

About **68 machines** (6.8%) would experience at least one component failure in the first 30 days. The most likely culprit? The motherboard, followed by the CPU.

### 3-Year Survival

| Component | 3-Year Failure Rate | Survival Rate |
|---|---|---|
| CPU | 2.5% | 97.5% |
| GPU | 2.0% | 98.0% |
| Motherboard | 4.0% | 96.0% |
| RAM (x2 sticks) | 1.0% combined | 99.0% |
| NVMe SSD | 1.0% | 99.0% |
| PSU | 1.5% | 98.5% |
| Cooler | 1.5% | 98.5% |
| NIC (onboard) | 1.0% | 99.0% |

**P(all components survive 3 years)** = 0.975 × 0.98 × 0.96 × 0.99 × 0.99 × 0.985 × 0.985 × 0.99

**≈ 0.860**

### 3-Year Result: ~860 out of 1,000 PCs working perfectly

About **140 machines** (14%) would have experienced at least one component failure by the 3-year mark.

<svg id="survivalChart" class="my-8"></svg>
<p class="text-center text-sm text-gray-600 -mt-4">
    <strong>Note:</strong> "Working perfectly" means zero component failures. Many failed systems would have only a single dead part (e.g., a bad RAM stick) and could be repaired with a single swap.
</p>

### What Breaks Most Often?

<svg id="contributionChart" class="my-8"></svg>
<p class="text-center text-sm text-gray-600 -mt-4">
    Each bar shows the individual component's contribution to the ~14% overall 3-year system failure probability. The motherboard alone accounts for nearly a third of all expected failures.
</p>

## Summary

| Timeframe | PCs with Zero Failures (out of 1,000) | PCs with At Least One Failure |
|---|---|---|
| **30 days** | **~932** | ~68 |
| **3 years** | **~860** | ~140 |

The single largest contributor to system failure is the **motherboard** at ~4%, followed by the **CPU** at ~2.5% and the **GPU** at ~2%. RAM and SSDs are remarkably reliable, contributing very little to overall system failure probability.

## Caveats and Limitations

1. **Independence assumption.** We treat component failures as independent. In reality, a PSU failure (voltage spike, ripple) can cascade and damage the motherboard, CPU, or GPU. Conversely, a cheap case with poor airflow raises temperatures for *every* component.

2. **Consumer vs. professional data.** Puget Systems uses conservative BIOS settings, quality components, and professional assembly. A self-builder using default motherboard settings (especially aggressive Intel power profiles) would likely see **higher** CPU and motherboard failure rates.

3. **"Working perfectly" is strict.** We count any hardware failure. Many 3-year "survivors" will have degraded fans, slightly higher SSD wear, or intermittent issues (like Intel 2.5GbE connection drops) that don't constitute outright failure.

4. **Survivorship in the data.** Backblaze's fleet and Puget's customers represent curated populations. Backblaze buys enterprise drives; Puget selects components after reliability vetting. Consumer-grade builds with budget components may fare worse.

5. **Environmental factors.** Ambient temperature, humidity, power grid quality, and dust accumulation significantly affect component longevity but are not captured in these datasets.

6. **Brand and Model Variance.** The failure rates presented are generalized averages. Actual reliability can vary significantly between manufacturers and even specific product lines from the same brand. A premium component from a reputable brand may perform better than these averages, while a budget part may perform worse.

7. **Data Gaps.** While we've aggregated data from the best public sources, comprehensive, apples-to-apples failure rate data for every consumer component is scarce. Some figures, especially for newer or less-tracked components, are based on limited data or extrapolation.

## Practical Recommendations

- **Test thoroughly in the first 30 days.** Run stress tests (Prime95, FurMark, memtest86+) early. The bathtub curve is your friend — most defective parts will reveal themselves quickly.
- **Use JEDEC RAM speeds** unless you need XMP. Overclocked memory dramatically increases failure risk.
- **Invest in the PSU.** A quality PSU protects every other component. The failure rate difference between a budget and premium PSU is significant.
- **Check your motherboard's Ethernet controller.** If it uses an Intel I225-V or I226-V, apply the EEE workaround immediately <a href="https://www.tomshardware.com/news/intel-patches-stuttering-ethernet-issues-but-its-just-a-workaround-for-now">[15]</a>.
- **Don't cheap out on the motherboard.** It has the highest failure rate of any component, and a failure often takes the whole system down.
- **Keep an SSD-only build if possible.** HDDs have 4x the 3-year failure rate of NVMe SSDs and add noise, heat, and vibration.

## References

1. <a href="https://en.wikipedia.org/wiki/Bathtub_curve">"Bathtub Curve." Wikipedia.</a>
2. <a href="https://www.itl.nist.gov/div898/handbook/apr/section1/apr124.htm">"8.1.2.4 Bathtub Curve." NIST Engineering Statistics Handbook.</a>
3. <a href="https://forums.tomshardware.com/threads/chances-of-getting-a-doa-mobo.621254/">"Chances of Getting a DOA Mobo?" Tom's Hardware Forums.</a>
4. <a href="https://www.pugetsystems.com/labs/articles/puget-systems-most-reliable-hardware-of-2024/">"Puget Systems Most Reliable Hardware of 2024." Puget Systems, January 2025.</a>
5. <a href="https://www.pugetsystems.com/labs/articles/most-reliable-pc-hardware-of-2021-2279/">"Most Reliable PC Hardware of 2021." Puget Systems.</a>
6. <a href="https://hothardware.com/news/gpu-mb-failure-rates-digitec-galaxus">"GPU and Motherboard Failure Rates at Swiss PC Store Highlight Most Reliable Brands." HotHardware.</a>
7. <a href="https://www.tomshardware.com/news/retailer-shares-failure-rates-for-gpus-motherboards-ssds-more">"Retailer Shares Failure Rates for GPUs, Motherboards, SSDs, More." Tom's Hardware.</a>
8. <a href="https://www.backblaze.com/blog/backblaze-drive-stats-for-2024/">"Hard Drive Failure Rates: The Official Backblaze Drive Stats for 2024." Backblaze, February 2025.</a>
9. <a href="https://www.backblaze.com/blog/ssd-edition-2023-mid-year-drive-stats-review/">"SSD Edition: 2023 Drive Stats Mid-Year Review." Backblaze, September 2023.</a>
10. <a href="https://www.pcworld.com/article/394099/ryzen-5000-failure-rates-we-reality-check-the-claims.html">"Ryzen 5000 Failure Rates: We Reality-Check the Claims." PCWorld.</a>
11. <a href="https://www.xda-developers.com/worst-pc-hardware-failures-2024/">"7 Worst PC Hardware Failures of 2024." XDA Developers.</a>
12. <a href="https://flexpowermodules.com/resources/fpm-designnote002-power-supply-reliability-aspects">"Reliability Aspects on Power Supplies." Flex Power Modules, Design Note 002.</a>
13. <a href="https://forum.netgate.com/topic/100700/onboard-intel-or-external-nic">"OnBoard Intel or External NIC." Netgate Forum.</a>
14. <a href="https://hardforum.com/threads/intel-1226-v-2-5gbe-ethernet-chipset-showing-connection-drop-issues-chipset-used-on-most-raptor-lake-motherboards.2025009/">"Intel 1226-V 2.5GbE Ethernet Chipset Showing Connection Drop Issues." [H]ard|Forum.</a>
15. <a href="https://www.tomshardware.com/news/intel-patches-stuttering-ethernet-issues-but-its-just-a-workaround-for-now">"Intel Patches Stuttering Ethernet Issues, but It's Just a Workaround for Now." Tom's Hardware.</a>
16. <a href="https://www.cxtec.com/blog/network-hardware-failures-shocking-truth/">"Surprising Truth About Network Hardware Failures." CXtec.</a>

<script src="https://cdn.jsdelivr.net/npm/chart.xkcd@1.1/dist/chart.xkcd.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded', function () {
    // Chart 0: Bathtub Curve
    var bathtubData = [];
    for (var t = 0; t <= 10; t += 0.25) {
        var infantMortality = 3.5 * Math.exp(-1.5 * t);
        var wearOut = t > 5 ? 0.08 * Math.pow(t - 5, 2.2) : 0;
        var constant = 0.3;
        bathtubData.push({ x: t, y: infantMortality + constant + wearOut });
    }
    new chartXkcd.XY(document.getElementById('bathtubCurveChart'), {
        title: 'The Bathtub Curve: Component Failure Rate Over Time',
        xLabel: 'Time (Years)',
        yLabel: 'Failure Rate',
        data: {
            datasets: [{
                label: 'Failure Rate',
                data: bathtubData,
            }, {
                label: 'invisible',
                data: [{ x: 0, y: 0 }],
                options: { showLine: false }
            }]
        },
        options: {
            xTickCount: 10,
            yTickCount: 5,
            legendPosition: chartXkcd.config.positionType.upRight,
            showLine: true,
            timeFormat: undefined,
            dotSize: 0.3,
        }
    });

    // Chart 1: 3-Year Failure Rates by Component (sorted descending)
    new chartXkcd.Bar(document.getElementById('failureRateChart'), {
        title: '3-Year Failure Rate by Component (%)',
        xLabel: 'Component',
        yLabel: 'Failure Rate (%)',
        data: {
            labels: ['Mobo', 'HDD', 'CPU', 'GPU', 'PSU', 'Cooler', 'NIC', 'SSD', 'RAM (x2)'],
            datasets: [{
                data: [4.0, 4.0, 2.5, 2.0, 1.5, 1.5, 1.0, 1.0, 1.0],
            }]
        },
        options: {
            yTickCount: 5,
        }
    });

    // Chart 2: 1,000 PCs Survival
    new chartXkcd.Bar(document.getElementById('survivalChart'), {
        title: 'Out of 1,000 PCs Built: How Many Survive?',
        xLabel: '',
        yLabel: 'Number of PCs',
        data: {
            labels: ['Day 0', '30 Days', '3 Years'],
            datasets: [{
                data: [1000, 932, 860],
            }]
        },
        options: {
            yTickCount: 5,
        }
    });

    // Chart 3: Component Contribution to 3-Year Failure (sorted descending)
    new chartXkcd.Bar(document.getElementById('contributionChart'), {
        title: 'Which Component Kills Your PC? (3-Year Failure Rate %)',
        xLabel: 'Component',
        yLabel: 'Failure Rate (%)',
        data: {
            labels: ['Motherboard', 'CPU', 'GPU', 'PSU', 'Cooler', 'NIC', 'SSD', 'RAM (x2)'],
            datasets: [{
                data: [4.0, 2.5, 2.0, 1.5, 1.5, 1.0, 1.0, 1.0],
            }]
        },
        options: {
            yTickCount: 5,
        }
    });
});
</script>
