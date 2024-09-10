# Reproducibility and Uncertainty Assessment in EQTransformer

<a id="readme-top"></a>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- PROJECT DESCRIPTION -->
## Article Abstract

This study evaluates the performance and reliability of earthquake detection using EQTransformer, a novel AI program widely used in seismological observatories and research to enhance earthquake catalogs. We tested EQTransformer's capabilities and uncertainties using seismic data from the Volcanological and Seismological Observatory of Costa Rica, comparing two detection methods: the simplified method (MseedPredictor) and the complex method (Predictor), which incorporates Monte Carlo Dropout, to assess reproducibility and uncertainty in identifying seismic events.

Our analysis focuses on 24-hour data starting on February 18, 2023, following a magnitude 5.5 mainshock. Sequential experiments with identical data and parametrization yielded different detections and a varying number of events over time. The results demonstrate that the complex method, which leverages iterative dropout, consistently provides more reproducible and reliable detections than the simplified method, which shows greater variability and is more prone to false positives.

This study highlights the importance of method selection in deep learning models for seismic event detection, emphasizing the need for rigorous evaluation of detection algorithms to ensure accurate and consistent earthquake catalogs. Our findings offer valuable insights into the application of AI tools in seismology, particularly in enhancing the precision and reliability of seismic monitoring efforts.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Built With

This research utilized various codes and tools, some developed by us, alongside EQTransformer [Mousavi, 2020]. As this research extends the OKSP workflow developed in 2021 [Van der Laat, 2021], we provide the necessary tools, code, and data to reproduce our results.

### Hardware Requirements
- **Operating System:** Linux 64-bit (cluster, server, or personal computer).
- **GPU Recommendation:** NVIDIA GPU for faster results.

### Programming Language
- **Python:** All scripts and tools are developed in Python 3.

### Prerequisites

#### Conda Environment:
We recommend working within a Conda environment for consistency and ease of reproduction. We provide a clone of our environment. Detailed instructions for setting up Conda can be found in this tutorial:  
[Conda on the Cluster](https://github.com/um-dang/conda_on_the_cluster.git)

#### EQTransformer:
The EQTransformer tool can be accessed by cloning the following repository:  
[EQTransformer GitHub](https://github.com/smousavi05/EQTransformer.git)

**Note:** We strongly recommend using our provided Conda environment as it contains updated software libraries actively used in this research.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Installation and Running

Follow these steps to set up the project:

1. Clone this repository:
   ```bash
   git clone https://github.com/SebasGamboa10/Reproducibility-and-Uncertainty-Assessment-in-EQTransformer.git
   ```
   
2. Create the Conda environment:
   ```bash
   conda create -n eq_env --file eq_env.txt
   ```

3. Access the `Source_Code` folder:
   ```bash
   cd Source_Code
   ```

4. Open the `params.txt` file and modify it according to your execution needs:
   ```bash
   /Path/Source_Code /Path/EQTransformer /Path/Output_Folder /Path/DATA /Path/stations Year Day Day
   ```

5. Run the project automatically using the following commands:
   ```bash
   # First time only:
   chmod +x ./run.sh
   ./run.sh
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Analysis Code, Comparison and Plots

In the folder: Experimental_Results/Results_Analysis_Code

1. For comparison of the results, use the code:
   * Experimental_Results/Results_Analysis_Code/compare.py

2. For generating time plots, use the code:
   * Experimental_Results/Results_Analysis_Code/time_plot.py

3. For generating histograms, use the code:
   * Experimental_Results/Results_Analysis_Code/histogram_plot.py

4. For generating heatmaps, use the code:
   * Experimental_Results/Results_Analysis_Code/heatmap.py

5. For generating donut plots, use the following codes:
   * Experimental_Results/Results_Analysis_Code/Complex_method_donut_chart_plot.py
   * Experimental_Results/Results_Analysis_Code/Simplified_method_donut_chart_plot.py


Additionally, for plotting the Monte Carlo iterations graph, use the code: 
* Experimental_Results/MC_Dropout_Iterations/mc_iteration_plot.py

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Important:
If you want to switch from `Predictor` (Complex) to `MseedPredictor` (Simplified), edit `deteccion.sh` on line 5:
   ```bash
   # Complex execution method:
   python3 "mydir/EQT_DETECT_PREDICTOR.py" ...

   # Simplified execution method:
   python3 "mydir/EQT_DETECT_PREDICTOR.py" ...
   ```

If you run both methods for comparison, use different output folders to avoid overwriting results.

## Authors

- **Sebastián Gamboa Chacón**  
  Costa Rica Institute of Technology and National High Technology Center  
  [sgamboa@cenat.ac.cr](mailto:sgamboa@cenat.ac.cr)

- **Esteban Meneses**  
  Costa Rica Institute of Technology and National High Technology Center  
  [emeneses@cenat.ac.cr](mailto:emeneses@cenat.ac.cr)

- **Esteban J. Chaves Sibaja**  
  National University of Costa Rica - Volcanological and Seismological Observatory of Costa Rica  
  [esteban.j.chaves@una.ac.cr](mailto:esteban.j.chaves@una.ac.cr)

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

For any inquiries or additional support, please contact us at:

- **Email:** [sgamboa@cenat.ac.cr](mailto:sgamboa@cenat.ac.cr)
- **GitHub:** [SebasGamboa10](https://github.com/SebasGamboa10)
- **Phone:** +506 6098 1011

Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Acknowledgments

This research was partially supported by a machine allocation on the Kabré supercomputer at the Costa Rica National High Technology Center.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
