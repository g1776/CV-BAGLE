# CV-BAGLE
## Computer Vision-BAsed Glyph And Label Extraction
 DS 340W Final Project

![CV-BAGLE](https://c.tenor.com/mOI0fyd2QpYAAAAd/laptop-bagel-net.gif)

### File Structure

- src
    - models
        - Contains the classification models (not included in repo)
    - features
        - eval
            - GLE performance evaluation. (Figures IV and V in the paper)
        - extraction
            - GLE Implementation.
        - gen
            - Synthetic dataset generation.
- volume
    - processed
        - Contains the Glyph and Label features dataset calculated for all of the training data, as well as the GLE metrics dataset.
    - raw
        - The synthetic dataset
    - test
        - Real-world data, in the same format as `/raw`.
