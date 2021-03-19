# TODO

- [ ] Go through ISC Python tutorial
- [ ] Organize data
- [-] Get cognitive measures (aka labels)
- [ ] Download release 9 from HBN (maybe not as kids with covid may affect fMRI results due to respiratory condition)
- [ ] Try using ISC in analysis
- [ ] Test simple ML models
- [ ] Read more literature
- [ ] Sort out Mendeley literature
- [ ] Remove duplicate subject "sub-NDARFU786BN4" in ages 9, 14, 15

- Explore FC changes over ages
- Explore FC correlation with cognitive measures
- Explore FC into CNN to predict cognitive measures
- Explore ISC
- Explore compression algorithm on FC
- Explore models lsvc, dnn, ica

- Multivariate regression (once I can predict IQ well, predicting multiple labels)
- Age bins
- For PCA, separate ages
  - Kinda done
- Run PCA for different components until explained variance is high
  - With 50 PCA components, I get an explained variance = 0.61 and an r^2 = 0.11.
- Try getting rid of outlier
- Try combining cognitive measures to amplify effect of executive function
  - FSIQ already combines it
  - WIAS for ages above 16 so not considering it
- Try different components of ICA, Use ica on the saveresids files, not the FC (Have to cross validate to not make it circular)
- Another dimensionality reduction is to take the 15 strongest connections
- Superimpose Yeo template and then only take the connections within the fronto-parietal network , DMN, FP <-> DMN
- Look for demographic variables
- Add Kathleen dataset (add it as the testing set)
- Keep the feature space but feature selection (don't reduce/compress).
  - Filter methods, feature selection, rank the features
  - Mutual information
- Too many noisy variables, remove them but also keep the informative ones
- Use brain volume
- It's unclear what's involved in the executive network.
- Huge divide between labels and brain functions. What are the mechanisms that differentiate these abilities?
- Take the individual scores and combine them in a way we believe is meaningful
- Instead of IQ, if we used a subtest, would we get different results?
- Yeo connectivity networks related to IQ?

- ICA on Kathleen clean
- Try another WISC score
- YEO -> Frontal-parietal -> Recompute for DMN and FPN (within and across) -> Mean -> 3 numbers -> LR
- How many Power nodes are in each Yeo network
- Check distribution before calculating mean
- Try simple ML model
- Summarize meeting with Bobby and send to Yalda

- Continue reading papers
- Class balancing in regression tasks
- Analysis issues with dataset or with the methods

- Is ML needed for mapping functional connectivity to IQ?
- For linear models, you need one number for one person
- Use kernel methods, SVR (support vector regression). Data space -> Kernel space
- Give context of images sent to
- Revisit PLS paper and add in testing set
- Read Brandon papers for the methods
- 19 islands in Yeo network
- Regression within FPN, within DMN, between FPN+DMN
- Threshold Yeo FC matrix and use SVR on the multiple features
- *Model comparison: Data-driven SVR vs Hypothesis-driven SVR (try different labels)
  - Use BCR
- Then try ANN model
- Temporal FC by splitting the movie fmri into windows of 1 minute

- Run PLS like the paper and identify num of components (75%)
- Then use age as one of the labels instead of IQ
  - IQ may not be represented in brain connectivity (but we can't say it isn't)
  - We can say that FC is more strongly related to age than IQ
  - **Check WISC IQ and how they scale it** Dive into IQ and see its relationship with age
  - Use percentile rank for IQ
  - Instead of using IQ, use one of the test scores instead (working memory)
  - Plot working memory against age to confirm
- Try SVR on age instead of IQ
- Read general cog dev

- Run correlations for raw and scaled scores
- Use PLS with raw score (digit span) and scaled score, and see if the results disappear
- One way to disentangle age from cognitive scores is to use the scaled scores
- See how they calculate IQ
- Puberty onset score in HBN (include as a regressor)
- Remove HBN data from Github
