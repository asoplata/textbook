<!--
# Title: 3.2 Optimization in the GUI
# Updated: 2026-07-28
#
# Contributors:
    # Nicholas Tolley
    # Austin E. Soplata
-->

# 3.2 Optimization in the GUI

## Tutorial Table of Contents

1. [Background](#toc-1)

2. [Section 1: Identify a Treatment-Induced EEG ERP Biomarker and Define Model Hypotheses](#toc-2)

3. [Section 2: Initialize the Default HNN Model — Install Modeling Software and Set Up the Project Folder](#toc-3)

4. [Section 3: Establish Pre-Treatment Model Fit with Manual Tuning](#toc-4)

5. [Section 4: Establish Pre-Treatment Model Fit with Parameter Optimization](#toc-5)

6. [Section 5: Establish Post-Treatment Model Fit](#toc-6)

7. [Where to Go From Here](#toc-7)

<a id="toc-1"></a>

## 1. Background

This tutorial walks through Sections 1 through 5 of the Protocol described in [@tolley_protocol_2026], published in the *Journal of Visualized Experiments* (JoVE). That paper demonstrates a hypothesis-driven workflow for using the Human Neocortical Neurosolver (HNN) to uncover the putative neural mechanisms underlying a neurotherapeutic's effect on an EEG biomarker.

The core idea is that many EEG/MEG biomarkers used in central nervous system (CNS) drug development — such as event-related potential (ERP) components — are only correlationally linked to the underlying disease state or drug effect. Statistical analyses of a biomarker can tell you *that* a treatment changed a signal, but not *which* cellular or circuit properties changed to produce that effect. Because HNN's neocortical column model directly links simulated current dipoles to specific cell- and circuit-level parameters (local connectivity, synaptic conductances, exogenous drive timing and strength, and dendritic ion channel conductances), fitting the model to pre-treatment and post-treatment EEG data lets you generate concrete, testable hypotheses about the treatment's mechanism of action.

The published protocol demonstrates this workflow using a hypothetical neurotherapeutic that reduces the P1, N1, and P2 components of an auditory evoked response. The pre-treatment ERP is real, source-localized MEG data from a previously published study [@kohl_neural_2022], and the "post-treatment" ERP is generated computationally for illustrative purposes by scaling the pre-treatment waveform.

The full protocol has seven sections. This tutorial covers the first five, which take you from identifying a biomarker all the way through fitting both a pre-treatment and a post-treatment model:

1. Identify a treatment-induced EEG ERP biomarker and define model hypotheses.
2. Initialize the default HNN model: install the modeling software and set up a project folder.
3. Establish a pre-treatment model fit using manual tuning.
4. Establish a pre-treatment model fit using automated parameter optimization.
5. Establish a post-treatment model fit.

Sections 6 (uncertainty quantification with simulation-based inference, SBI) and 7 (multiscale examination and validation) are not covered here; see the original paper for details on those steps.

<div class="callout callout-warning">
  <table class="callout-table">
    <tr>
      <td class="emoji-cell">
        <svg class="exclamation-icon" viewBox="0 0 16 16" width="20" height="20">
            <path d="M15.35 12.81 9 2.08a1.22 1.22 0 0 0-2 0L.65 12.81a1.14 1.14 0 0 0 1 1.69h12.66a1.14 1.14 0 0 0 1.04-1.69zm-13.66.55L8 2.64l6.31 10.72z"/>
            <path d="M7.32 5.45h1.25V10H7.32z"/>
            <ellipse cx="7.95" cy="11.9" rx=".67" ry=".7"/>
        </svg>
      </td>
      <td class="text-cell">
      This tutorial closely follows the wording and step numbering of the original published Protocol so that you can cross-reference the two easily. All data files, code, and configuration files referenced below are hosted in the paper's associated code repository at <a href="https://github.com/ntolley/hnn_jove">github.com/ntolley/hnn_jove</a>.
    </td>
      <td class="emoji-cell"> </td>
    </tr>
  </table>
</div>

<a id="toc-2"></a>

## 2. Section 1: Identify a Treatment-Induced EEG ERP Biomarker and Define Model Hypotheses

This first section does not involve HNN directly. Instead, it establishes the empirical biomarker and the biological hypotheses you will later translate into HNN model parameters.

1. Collect or identify a dataset containing experimentally recorded EEG signals from subjects of interest (e.g., pre-treatment and post-treatment in the context of neurotherapeutics). Record EEG measurements during presentation of a sensory stimulus, and record timestamps of the sensory stimulus simultaneously with the EEG data to enable segmentation into trials. Ensure that EEG data are stored in a format compatible with preprocessing software (e.g., `.fif`, `.set`, or `.edf`).

2. Identify a set of candidate ERP biomarker features that are hypothesized to distinguish treatment-related effects (e.g., ERP peak timings and magnitudes).

3. Preprocess the EEG data and extract the biomarker features of interest.
    1. Perform source localization using sensor-level signals from all channels, or select EEG sensors to be analyzed. Use source-localized data for direct comparison with model output, since sensor-level data will not have unit correspondence.
    2. Segment the recorded EEG data into trials using the timestamps of the sensory stimulus.
    3. Compute trial-averaged ERP waveforms for the pre-treatment and post-treatment conditions.
    4. Extract candidate ERP biomarkers from the trial-averaged waveforms (e.g., compute N1 peak magnitudes). Define peak detection criteria (e.g., time window and polarity) prior to extraction.

4. Conduct statistical tests to determine which ERP features are significantly different across conditions (e.g., pre-treatment versus post-treatment). Select appropriate statistical tests based on study design, and apply multiple-comparison correction where necessary (e.g., repeated-measures ANOVA followed by Tukey HSD post-hoc testing).

5. Output specific statistically significant distinguishing EEG biomarker features (e.g., differences in N1 magnitudes). Save outputs for use in subsequent steps.

6. Define literature-based hypotheses on drug mechanisms and associated model parameters of interest. Consult prior literature and experimental data to identify biophysical properties altered by the neurotherapeutic that may account for the feature differences identified in Step 4.

7. Identify which parameters of the biophysical neural model (HNN) are directly represented or indirectly related to the biological properties identified in Step 6. Map biological mechanisms to model parameters using prior literature and HNN documentation.

8. Output an identified set of model parameters of interest corresponding to biophysical properties hypothesized to generate the identified EEG feature differences. Use the default HNN model (initialized in [Section 2](#toc-3)) as the starting point for all parameter values, and save outputs for use in subsequent steps.

The associated code repository provides the pre-treatment and post-treatment data files used to generate this tutorial's representative results. The pre-treatment ERP is a preprocessed auditory MEG ERP from Kohl et al. (2022) [@kohl_neural_2022] (original data available at [github.com/kohl-carmen/HNN-AEF](https://github.com/kohl-carmen/HNN-AEF)). The hypothetical post-treatment ERP is generated by scaling the pre-treatment waveform using a Gaussian-tapered window. Both files are located in the repository at `data/pre-treatment.txt` and `data/post-treatment.txt`.

<a id="toc-3"></a>

## 3. Section 2: Initialize the Default HNN Model — Install Modeling Software and Set Up the Project Folder

1. Download and install a functioning version of Anaconda Python. Create and activate a new Python environment for the installation of required software packages.

2. Install the biophysical neural modeling `hnn-core` software using the operating-system-specific installation instructions available on the [Installation page](../01_getting_started/installation.html). To efficiently install the software dependencies used in the original study, the associated code repository ([github.com/ntolley/hnn_jove](https://github.com/ntolley/hnn_jove)) uses [pixi](https://pixi.prefix.dev/latest/); follow the instructions in the repository's `README` file to install pixi and set up a local version of the code repository.

3. Verify that the installed version of the biophysical neural modeling software is `0.6.0` or greater by typing the following command into the terminal:

    ```
    pip show hnn_core
    ```

4. Ensure that the Python environment is activated and that installation completed successfully. Launch the graphical user interface (GUI) by typing `hnn-gui` in the terminal and pressing Enter.

5. Create a new project folder on the computer file system to store all data files generated in this protocol. Create the folder in an accessible directory (e.g., home directory or working project directory).

<a id="toc-4"></a>

## 4. Section 3: Establish Pre-Treatment Model Fit with Manual Tuning

1. Start with the canonical HNN ERP simulation and its default parameters. Manually tune the scaling factor and exogenous drive parameters to fit the pre-treatment ERP identified in [Section 1](#toc-2). The HNN GUI automatically loads model parameters fit to a somatosensory ERP, which through numerous studies has been shown to be a good "canonical ERP" starting point; this tutorial focuses on modifying the scaling factor and exogenous input parameters from that starting point.

2. Load the pre-treatment empirical ERP waveform into the HNN GUI.
    1. Click the `Load data` button on the menu bar located on the lower left portion of the GUI window.
    2. In the file browser window, select a `.csv` or `.txt` file containing the ERP waveform to be modeled (i.e., the target waveform, `pre-treatment.txt` in the associated code repository). Ensure that the file is comma-delimited and formatted with two columns: the first contains time (ms), and the second contains the source-localized empirical dipole waveform (nAm). The first row is treated as a header and should not contain data values. Informative column labels (e.g., "Time (ms)" and "Dipole (nAm)") may optionally be included.
    3. Inspect the waveform that is automatically plotted in the figure panel.

3. Run the default simulation of a canonical ERP.
    1. Set the parameter values of `tstop`, `dt`, `Trials`, `Backend`, and `Cores` in the Simulation Parameters panel to the desired values. Use `tstop` to control the simulation length, `dt` to control the integration time-step, and `Trials` to control the number of repeated simulations run with the same model parameter values. Select `Backend` as either serial (Joblib) or parallel (MPI), and specify the number of computer `Cores`. Variability across trials comes from the standard deviation of the exogenous evoked drive timing described in Step 6 below.
    2. Click the `Run` button to start the default simulation of a canonical ERP.

4. Create a plot that compares the simulated ERP to the empirical ERP.
    1. Click the `Visualization` tab on the top left of the GUI window.
    2. Click the dropdown menu labeled `Data to compare` and select the loaded target waveform from Step 2.2.
    3. Click `Clear axis` to reset the plot.
    4. Click `Add plot` to generate a new plot with the simulated initial ERP waveform (blue) and target waveform (orange) overlaid, along with text indicating the automatically calculated correlation coefficient (Corr) and root mean squared error (RMSE) between the two waveforms. The HNN GUI provides the option to calculate these two goodness-of-fit measures, which are used for manual hand tuning and for optimization in [Section 4](#toc-5).

5. Modify the scaling factor. Modify the scaling factor by manual hand tuning to approximately match the magnitudes of the simulated and empirical dipole waveforms. Set the default `Dipole scaling` parameter in the Simulation tab to `3000`. The scaling factor corresponds to a prediction of the estimated number of neurons underlying the generation of the EEG signal: the default value of 3000 indicates that 200 pyramidal neurons (the size of the HNN model) &times; 3000 = 600,000 neurons are necessary to generate an evoked response with the magnitude in nAm indicated on the y-axis.

6. Modify timing of exogenous drives. Modify the mean and standard deviation of exogenous drives by manual hand tuning to obtain a closer fit to the timing of the empirically recorded pre-treatment ERP peaks (i.e., P1/N1/P2). The default local connectivity and cell parameters distributed with HNN were tuned to reproduce healthy single-cell and network-level activity patterns; it is recommended to leave the pre-tuned local HNN neocortical template model parameters fixed initially and test whether a reliable fit can be achieved by adjusting only the exogenous drives.
    1. Identify which simulated ERP peaks are misaligned in time with the empirical ERP waveform. This example assumes three early peaks in the empirical ERP, as in the default canonical ERP simulation; to add peaks, simulate additional external drives.
    2. Click the `External drives` tab on the top left of the GUI window. The parameters for three predefined exogenous drives are visible, representing the feedforward proximal (`evprox1`), feedback distal (`evdist1`), and re-emergent feedforward proximal (`evprox2`) drives that generate the default canonical ERP simulations, along with spike histograms depicting their timing and counts.
    3. Click on the dropdown of the exogenous drive whose `Mean time` is closest to the misaligned peak.
    4. Modify the values in the text boxes for `Mean time` and `Std dev time` to better match the timing and width of peaks in the target waveform. Adjust `Mean time` to shift peak timing and `Std dev time` to change peak width. These parameters control the mean and variance of the exogenous spikes that activate the local network in proximal or distal projection patterns, but do not fully determine ERP peak timing or width — the exact timing and width also depend on intrinsic network activity.
        1. Set the `Mean time` for the `evprox1` external drive to `60 ms`.
        2. Set the `Mean time` for the `evdist1` external drive to `100 ms`.
        3. Set the `Mean time` for the `evprox2` external drive to `150 ms`.

7. Modify magnitude of exogenous drives. Modify synaptic weights (post-synaptic conductance) of exogenous drives by manual hand tuning to obtain a closer fit to the magnitude of the empirically recorded ERP peaks (i.e., P1/N1/P2).
    1. Identify which simulated ERP peaks are misaligned in magnitude with the empirical ERP waveform.
    2. Click the `External drives` tab on the top left of the GUI window.
    3. Click on the dropdown of the exogenous drive whose `Mean time` is closest to the misaligned peak.
    4. Modify the values in the text boxes under `AMPA weights` and `NMDA weights` to adjust synaptic conductances. Increasing proximal drive strength to L5 and L2/3 pyramidal neurons generally produces more positive peaks, while increasing distal drive strength generally produces more negative peaks. As with drive timing, ERP peak magnitude is not fully determined by drive strength — spiking dynamics can produce non-intuitive effects, so test changes over one order of magnitude (e.g., AMPA L5_pyramidal from 0.014 to 0.14) and refine iteratively.
        1. Set the `AMPA weights` of the `evdist1` drive to `L5_pyramidal` = `0.014243` and `L2_pyramidal` = `0.0000007`.
        2. Set the `NMDA weights` of the `evdist1` drive to `L5_pyramidal` = `0.0080074` and `L2_pyramidal` = `0.0004317`.
        3. Set the `AMPA weights` of the `evprox2` drive to `L5_pyramidal` = `0.0684013` and `L2_pyramidal` = `0.143884`.

    A complete set of parameters used to generate the representative results in the original paper is available in the associated code repository at `data/opt_baseline_config_correlation_best.json`. You are encouraged to load this configuration file along with the provided data files (`data/pre-treatment.txt` and `data/post-treatment.txt`) and refer to the example workflows in the `notebooks/` directory to reproduce the reported simulations.

8. Save modified simulation setup. After completing modifications in Steps 5–7, click the `Simulation` tab and enter `pre-treatment_handtuned` in the `Name` text box.

9. Run modified simulation.
    1. Click the `Run` button to simulate the modified parameter set.
    2. Inspect the generated plot in the figure panel. Access previous plots using the corresponding figure tabs (e.g., "Figure 1" and "Figure 2").

10. Iterate manual tuning. Continue iterative manual tuning to improve the correlation coefficient by repeating Step 4 to replot the simulation with the target waveform and recalculate the correlation coefficient.

11. Save final model outputs.
    1. Click the `Save Network` button to save the best-fit parameter set as a `.json` file named `pre-treatment_handtuned.json`.
    2. Click the `Save simulation` button to save a `.txt` file named `pre-treatment_handtuned.txt`, which contains the simulated dipole waveform.
    3. Move both files to the project folder created in Step 5 of [Section 2](#toc-3), and ensure that file names match the simulation name in the dropdown menu. Files are saved to the default download directory of the web browser used to run the GUI; move files manually or temporarily change the browser download directory.

The protocol can be paused after saving the simulation outputs. Resume by loading the saved configuration files into the software.

<a id="toc-5"></a>

## 5. Section 4: Establish Pre-Treatment Model Fit with Parameter Optimization

Control of random seeding for optimization is not currently available in the GUI. For reproducible optimization runs, use the Python API — the associated code repository contains an example implementation (see `code/baseline_optimization.py`), where a fixed random seed can be set by passing a seed parameter to the optimization function (e.g., `optim.fit(..., seed=123)`). This example shows how to optimize targeted parameters to estimate single values that produce a close fit to the waveform using CMA-ES. This is not to be confused with SBI (Section 6 of the original protocol): both approaches fit model parameters, but the primary output of SBI is a distribution of plausible values rather than a single point estimate.

For pre-treatment ERPs, start by optimizing exogenous drive parameters under the assumption that cell and local network connection parameters in the default HNN neocortical model are fixed. The multiscale prediction provided by HNN (Section 7 of the original protocol) provides targets for validation of this assumption. As new information becomes available to constrain model predictions, the HNN framework allows estimation of any set of parameters.

1. Open optimization settings.
    1. Click the `Optimization` tab on the top left corner of the GUI.
    2. Configure the settings of the optimization run, including the number of iterations, solver, and objective function. The default optimization settings (Objective function = "dipole_corr"; Solver = "cma") are appropriate for ERP waveforms, and this objective function maximizes the correlation coefficient between simulated and empirical waveforms. Because the correlation coefficient is a scale-free measure, when using "dipole_corr" you should adjust the scaling factor after optimization (Step 6.1 below); alternatively, use "dipole_rmse" to minimize RMSE, in which case the scaling factor remains fixed.
    3. Click on the Max iterations textbox and enter `100`.

2. Select parameters for optimization.
    1. Click on the dropdown menu of an exogenous drive whose parameters will be optimized.
    2. Select the drive parameters to be optimized by clicking the checkbox under `Optimized against?`.

3. Define parameter constraints. Specify the range of parameter values explored by the optimizer by entering values into the `Min` and `Max` textboxes under `Constraints (%)`. Default values of 20% are suitable for simulations that already have a high correlation coefficient (Corr &gt; 0.9); for example, applying a 20% range to a Mean time of 65.53 ms produces bounds of 52.42&ndash;78.64 ms. For poor initial fits, increase the Min and Max percentages, though the number of simulations required may increase significantly.

4. Run optimization. Click the `Run Optimization` button to execute the optimization routine.

5. Save optimization results.
    1. Click the `Save Optimization History` button.
    2. Move the saved file to the project folder created in Step 5 of [Section 2](#toc-3). Optimization results can be stored and reused — the protocol may be paused at this stage and resumed by loading the saved optimization history.

6. Assess optimization quality. Evaluate the quality of the optimization run. When using correlation coefficient as the goodness-of-fit measure, a stopping criterion of Corr &gt; 0.95 is recommended, as this generally reflects a simulated waveform that reproduces the prominent peaks and troughs of the target ERP. Early stopping is not currently supported but is under development; increase the number of iterations if the stopping criterion is not met but the loss continues to decrease every 10 iterations. As noted above, when "dipole_corr" is used as the objective function, re-adjust the scaling factor after optimization — in the original paper's example, the scaling factor was reduced from the default of 3000&times; to 1000&times;.
    1. If optimization fails to achieve a good fit to the pre-treatment ERP, return to Step 2 and perform troubleshooting by increasing the maximum iterations, improving the manually tuned starting point, or selecting alternative parameters to adjust.

7. Determine next steps based on optimization outcome. If a good fit to the pre-treatment ERP is achieved (i.e., Corr &gt; 0.95), re-adjust the scaling factor to minimize RMSE and proceed to [Section 5](#toc-6).

<a id="toc-6"></a>

## 6. Section 5: Establish Post-Treatment Model Fit

1. Start with the optimized pre-treatment ERP simulation. Manually tune and optimize the parameters of interest to fit the post-treatment ERP.

2. Load the post-treatment empirical ERP waveform from [Section 1](#toc-2) into the GUI, using the same procedure as Step 2 of [Section 3](#toc-4).

3. Load the optimized pre-treatment ERP parameters from [Section 3](#toc-4) and [Section 4](#toc-5) as a starting point.

4. Perform manual tuning and optimization. Perform manual hand tuning and parameter optimization (the same procedures as Steps 2–11 of [Section 3](#toc-4) and all of [Section 4](#toc-5)) on the parameters of interest identified in Step 7 of [Section 1](#toc-2). Continue tuning and optimization until a high correlation (Corr &gt; 0.95) between the simulated and post-treatment ERP is achieved.

    In the original paper, hand tuning was applied to a single signal-targeted parameter (decreased local network GABA<sub>B</sub> maximal conductance), which produced a closer fit to the post-treatment data. Optimization was not performed to evaluate how well this one parameter change accounts for the data. Simulation-based inference (SBI, Section 6 of the original protocol) is recommended for rigorous investigations because it estimates distributions of parameters that account for an ERP waveform, enabling more robust comparisons across parameter fits than a single point-estimate fit.

5. Save model configuration and compare parameters.
    1. Save the model configuration and compare optimized values for parameters of interest between the pre-treatment and post-treatment conditions.
    2. Repeat Step 11 of [Section 3](#toc-4) to export a `.json` file of model parameters, and move the file to the project folder created in Step 5 of [Section 2](#toc-3).
    3. View exogenous drive parameters by clicking `Load external drives` and selecting either the pre-treatment or post-treatment network configuration file.
    4. View local network parameters by clicking `Load local network connectivity` and selecting either the pre-treatment or post-treatment network configuration file.
    5. Identify changes in parameter values across the pre-treatment and post-treatment network configurations, and interpret these changes as model-based predictions of post-treatment biomarker mechanisms.

<a id="toc-7"></a>

## 7. Where to Go From Here

At this point you have a pre-treatment model fit (Sections 3–4) and a post-treatment model fit (Section 5) built from the same default HNN network, differing only in the parameters you identified as hypothesized mechanisms of the neurotherapeutic. Comparing the fitted parameter values between the two conditions constitutes your first model-based prediction of how the treatment altered the underlying neural circuit.

The original protocol continues in two further sections not covered by this tutorial:

- **Section 6** uses simulation-based inference (SBI) to estimate full *distributions* of plausible parameter values for both conditions, rather than single best-fit point estimates, and quantifies how separable the pre- and post-treatment distributions are using an overlap index (OVL).
- **Section 7** demonstrates how to examine multiscale model predictions (e.g., cell-level spiking underlying the fitted dipole) that can subsequently be validated or further constrained by new empirical data, such as invasive electrophysiology or laminar MEG/EEG.

If you want to reproduce the exact representative results shown in the paper, or adapt the SBI and validation workflow to your own pre-/post-treatment data, see the associated code repository at [github.com/ntolley/hnn_jove](https://github.com/ntolley/hnn_jove), which includes the `code/`, `data/`, and `notebooks/` directories referenced throughout this tutorial.

For background on manually tuning and optimizing a somatosensory or auditory canonical ERP simulation outside of the neurotherapeutic-effects context of this protocol, see the [ERP Tutorial](../05_erps/erps_in_gui.html) and the [Optimize simulated evoked response parameters](09_optimize_simulated_evoked_response_parameters.html) tutorial.

## References
