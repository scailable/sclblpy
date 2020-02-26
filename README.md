# sclblpy
> Last edited 25-02-2020; McK.
> Effectively all functionality implemented **BUT** for the actual upload.

## Todo

1. Write tests for all models (e.g., test_all_models.py)
2. Discuss architecture w. Robin
3. Integrate toolchain.

## Info

Python package for Scailable uploads

Functionally this package allows one to upload fitted models to Scailable after authentication using JWT:
````
# Import the package:
import sclblpy as sp

# Fit a model
...

# Upload a model including documentation and an example feature vector
sp.upload(mod, docs, feature_vector)
````

Note that upon first upload the user will be prompted to provide the Scailable username and password 
(users can signup for an account at [https://www.scailable.net/admin/signup](https://www.scailable.net/admin/signup)).

## Further exposed functions
Next to the main ``upload()`` function, the package also exposes the following functions to administer endpoints:

````
# List all endpoints owned by the current user
sp.endpoints()

# Remove an endpoint
sp.delete_endpoint("cfid-cfid-cfid")
````

Finally, the package exposes

````
# Remove stored user credentials
sp.remove_credentials()

````

## Testing
Initial tests are available for all functionality. Run
````
python test_bundle.py
python test_jwt.py
python test_utils.py
python test_main.py
python test_all_models.py
````
inside ``/test/``. 

> Runnint the tests requires and active account.


## Notes:
Install package locally using ``pip install -e .``

## Dependencies
- ``requests``

# Currently supported models:

### StatsModels [[link](https://www.statsmodels.org/stable/about.html#about-statsmodels)]

| Name                      | Package     | Direct transpile (at 21-02-2020) | ONNX transpile (sometime 2020) |
| :------------------------ | :---------- | -------------------------------- | :----------------------------- |
| Generalized Least Squares | StatsModels | Yes                              |                                |
| Ordinary Least Squares    | StatsModels | Yes                              |                                |
| Weighted Least Squares    | StatsModels | Yes                              |                                |



### Scikit-learn [[link](https://scikit-learn.org/stable/)]


| Name                           | Package               | Direct transpile (at 21-02-2020) | ONNX transpile (sometime 2020) |
| :----------------------------- | :-------------------- | -------------------------------- | :----------------------------- |
| ARDRegression                  | linear_model          | Yes                              | Yes                            |
| AdaBoostClassifier             | ensemble              |                                  | Yes                            |
| AdaBoostRegressor              | ensemble              |                                  | Yes                            |
| AdditiveChi2Sampler            | kernel_approximation  |                                  |                                |
| AffinityPropagation            | cluster               |                                  |                                |
| AgglomerativeClustering        | cluster               |                                  |                                |
| BaggingClassifier              | ensemble              |                                  | Yes                            |
| BaggingRegressor               | ensemble              |                                  | Yes                            |
| BaseDecisionTree               | tree                  |                                  |                                |
| BaseEnsemble                   | ensemble              |                                  |                                |
| BayesianGaussianMixture        | mixture               |                                  | Yes                            |
| BayesianRidge                  | linear_model          | Yes                              | Yes                            |
| BernoulliNB                    | naive_bayes           |                                  | Yes                            |
| BernoulliRBM                   | neural_network        |                                  |                                |
| Binarizer                      | preprocessing         |                                  | Yes                            |
| Birch                          | cluster               |                                  |                                |
| CCA                            | cross_decomposition   |                                  |                                |
| CalibratedClassifierCV         | calibration           |                                  | Yes                            |
| CategoricalNB                  | naive_bayes           |                                  |                                |
| ClassifierChain                | multioutput           |                                  |                                |
| ComplementNB                   | naive_bayes           |                                  | Yes                            |
| DBSCAN                         | cluster               |                                  |                                |
| DecisionTreeClassifier         | tree                  | Yes                              | Yes                            |
| DecisionTreeRegressor          | tree                  | Yes                              | Yes                            |
| DictVectorizer                 | feature_extraction    |                                  | Yes                            |
| DictionaryLearning             | decomposition         |                                  |                                |
| ElasticNet                     | linear_model          | Yes                              | Yes                            |
| ElasticNetCV                   | linear_model          | Yes                              | Yes                            |
| EllipticEnvelope               | covariance            |                                  |                                |
| EmpiricalCovariance            | covariance            |                                  |                                |
| ExtraTreeClassifier            | tree                  | Yes                              | Yes                            |
| ExtraTreeRegressor             | tree                  | Yes                              | Yes                            |
| ExtraTreesClassifier           | ensemble              | Yes                              | Yes                            |
| ExtraTreesRegressor            | ensemble              | Yes                              | Yes                            |
| FactorAnalysis                 | decomposition         |                                  |                                |
| FastICA                        | decomposition         |                                  |                                |
| FeatureAgglomeration           | cluster               |                                  |                                |
| FeatureHasher                  | feature_extraction    |                                  |                                |
| FunctionTransformer            | preprocessing         |                                  | Yes                            |
| GaussianMixture                | mixture               |                                  | Yes                            |
| GaussianNB                     | naive_bayes           |                                  | Yes                            |
| GaussianProcessClassifier      | gaussian_process      |                                  |                                |
| GaussianProcessRegressor       | gaussian_process      |                                  | Yes                            |
| GaussianRandomProjection       | random_projection     |                                  |                                |
| GenericUnivariateSelect        | feature_selection     |                                  | Yes                            |
| GradientBoostingClassifier     | ensemble              |                                  | Yes                            |
| GradientBoostingRegressor      | ensemble              |                                  | Yes                            |
| GraphicalLasso                 | covariance            |                                  |                                |
| GraphicalLassoCV               | covariance            |                                  |                                |
| GridSearchCV                   | model_selection       |                                  | Yes                            |
| HuberRegressor                 | linear_model          | Yes                              | Yes                            |
| IncrementalPCA                 | decomposition         |                                  | Yes                            |
| IsolationForest                | ensemble              |                                  |                                |
| IsotonicRegression             | isotonic              |                                  |                                |
| KBinsDiscretizer               | preprocessing         |                                  | Yes                            |
| KMeans                         | cluster               |                                  | Yes                            |
| KNNImputer                     | impute                |                                  |                                |
| KNeighborsClassifier           | neighbors             |                                  | Yes                            |
| KNeighborsRegressor            | neighbors             |                                  | Yes                            |
| KNeighborsTransformer          | neighbors             |                                  |                                |
| KernelCenterer                 | preprocessing         |                                  |                                |
| KernelDensity                  | neighbors             |                                  |                                |
| KernelPCA                      | decomposition         |                                  |                                |
| KernelRidge                    | kernel_ridge          |                                  |                                |
| LabelBinarizer                 | preprocessing         |                                  | Yes                            |
| LabelEncoder                   | preprocessing         |                                  | Yes                            |
| LabelPropagation               | semi_supervised       |                                  |                                |
| LabelSpreading                 | semi_supervised       |                                  |                                |
| Lars                           | linear_model          | Yes                              | Yes                            |
| LarsCV                         | linear_model          | Yes                              | Yes                            |
| Lasso                          | linear_model          | Yes                              | Yes                            |
| LassoCV                        | linear_model          | Yes                              | Yes                            |
| LassoLars                      | linear_model          | Yes                              | Yes                            |
| LassoLarsCV                    | linear_model          | Yes                              | Yes                            |
| LassoLarsIC                    | linear_model          | Yes                              | Yes                            |
| LatentDirichletAllocation      | decomposition         |                                  |                                |
| LedoitWolf                     | covariance            |                                  |                                |
| LinearDiscriminantAnalysis     | discriminant_analysis |                                  | Yes                            |
| LinearRegression               | linear_model          | Yes                              | Yes                            |
| LinearSVC                      | svm                   | Yes                              | Yes                            |
| LinearSVR                      | svm                   | Yes                              | Yes                            |
| LocalOutlierFactor             | neighbors             |                                  |                                |
| LogisticRegression             | linear_model          |                                  | Yes                            |
| LogisticRegressionCV           | linear_model          |                                  | Yes                            |
| MLPClassifier                  | neural_network        |                                  | Yes                            |
| MLPRegressor                   | neural_network        |                                  | Yes                            |
| MaxAbsScaler                   | preprocessing         |                                  | Yes                            |
| MeanShift                      | cluster               |                                  |                                |
| MinCovDet                      | covariance            |                                  |                                |
| MinMaxScaler                   | preprocessing         |                                  | Yes                            |
| MiniBatchDictionaryLearning    | decomposition         |                                  |                                |
| MiniBatchKMeans                | cluster               |                                  | Yes                            |
| MiniBatchSparsePCA             | decomposition         |                                  |                                |
| MissingIndicator               | impute                |                                  |                                |
| MultiLabelBinarizer            | preprocessing         |                                  |                                |
| MultiOutputClassifier          | multioutput           |                                  |                                |
| MultiOutputRegressor           | multioutput           |                                  |                                |
| MultiTaskElasticNet            | linear_model          |                                  | Yes                            |
| MultiTaskElasticNetCV          | linear_model          |                                  | Yes                            |
| MultiTaskLasso                 | linear_model          |                                  | Yes                            |
| MultiTaskLassoCV               | linear_model          |                                  | Yes                            |
| MultinomialNB                  | naive_bayes           |                                  | Yes                            |
| NMF                            | decomposition         |                                  |                                |
| NearestCentroid                | neighbors             |                                  |                                |
| NearestNeighbors               | neighbors             |                                  | Yes                            |
| NeighborhoodComponentsAnalysis | neighbors             |                                  |                                |
| Normalizer                     | preprocessing         |                                  | Yes                            |
| NuSVC                          | svm                   | Yes                              | Yes                            |
| NuSVR                          | svm                   | Yes                              | Yes                            |
| Nystroem                       | kernel_approximation  |                                  |                                |
| OAS                            | covariance            |                                  |                                |
| OPTICS                         | cluster               |                                  |                                |
| OneClassSVM                    | svm                   |                                  | Yes                            |
| OneHotEncoder                  | preprocessing         |                                  | Yes                            |
| OneVsOneClassifier             | multiclass            |                                  |                                |
| OneVsRestClassifier            | multiclass            |                                  | Yes                            |
| OrdinalEncoder                 | preprocessing         |                                  | Yes                            |
| OrthogonalMatchingPursuit      | linear_model          | Yes                              | Yes                            |
| OrthogonalMatchingPursuitCV    | linear_model          | Yes                              | Yes                            |
| OutputCodeClassifier           | multiclass            |                                  |                                |
| PCA                            | decomposition         |                                  | Yes                            |
| PLSCanonical                   | cross_decomposition   |                                  |                                |
| PLSRegression                  | cross_decomposition   |                                  |                                |
| PLSSVD                         | cross_decomposition   |                                  |                                |
| PassiveAggressiveClassifier    | linear_model          | Yes                              | Yes                            |
| PassiveAggressiveRegressor     | linear_model          | Yes                              | Yes                            |
| Perceptron                     | linear_model          |                                  | Yes                            |
| PolynomialFeatures             | preprocessing         |                                  | Yes                            |
| PowerTransformer               | preprocessing         |                                  |                                |
| QuadraticDiscriminantAnalysis  | discriminant_analysis |                                  |                                |
| QuantileTransformer            | preprocessing         |                                  |                                |
| RANSACRegressor                | linear_model          |                                  | Yes                            |
| RBFSampler                     | kernel_approximation  |                                  |                                |
| RFE                            | feature_selection     |                                  | Yes                            |
| RFECV                          | feature_selection     |                                  | Yes                            |
| RadiusNeighborsClassifier      | neighbors             |                                  |                                |
| RadiusNeighborsRegressor       | neighbors             |                                  |                                |
| RadiusNeighborsTransformer     | neighbors             |                                  |                                |
| RandomForestClassifier         | ensemble              | Yes                              | Yes                            |
| RandomForestRegressor          | ensemble              | Yes                              | Yes                            |
| RandomTreesEmbedding           | ensemble              |                                  |                                |
| RandomizedSearchCV             | model_selection       |                                  |                                |
| RANSACRegressor                | linear_model          | Yes                              |                                |
| RegressorChain                 | multioutput           |                                  |                                |
| Ridge                          | linear_model          | Yes                              | Yes                            |
| RidgeCV                        | linear_model          | Yes                              | Yes                            |
| RidgeClassifier                | linear_model          |                                  | Yes                            |
| RidgeClassifierCV              | linear_model          |                                  | Yes                            |
| RobustScaler                   | preprocessing         |                                  | Yes                            |
| SGDClassifier                  | linear_model          | Yes                              | Yes                            |
| SGDRegressor                   | linear_model          | Yes                              | Yes                            |
| SVC                            | svm                   | Yes                              | Yes                            |
| SVR                            | svm                   | Yes                              | Yes                            |
| SelectFdr                      | feature_selection     |                                  | Yes                            |
| SelectFpr                      | feature_selection     |                                  | Yes                            |
| SelectFromModel                | feature_selection     |                                  | Yes                            |
| SelectFwe                      | feature_selection     |                                  | Yes                            |
| SelectKBest                    | feature_selection     |                                  | Yes                            |
| SelectPercentile               | feature_selection     |                                  | Yes                            |
| ShrunkCovariance               | covariance            |                                  |                                |
| SimpleImputer                  | impute                |                                  | Yes                            |
| SkewedChi2Sampler              | kernel_approximation  |                                  |                                |
| SparseCoder                    | decomposition         |                                  |                                |
| SparsePCA                      | decomposition         |                                  |                                |
| SparseRandomProjection         | random_projection     |                                  |                                |
| SpectralBiclustering           | cluster               |                                  |                                |
| SpectralClustering             | cluster               |                                  |                                |
| SpectralCoclustering           | cluster               |                                  |                                |
| StackingClassifier             | ensemble              |                                  |                                |
| StackingRegressor              | ensemble              |                                  |                                |
| StandardScaler                 | preprocessing         |                                  | Yes                            |
| TheilSenRegressor              | linear_model          | Yes                              | Yes                            |
| TransformedTargetRegressor     | compose               |                                  |                                |
| TruncatedSVD                   | decomposition         |                                  | Yes                            |
| VarianceThreshold              | feature_selection     |                                  | Yes                            |
| VotingClassifier               | ensemble              |                                  | Yes                            |
| VotingRegressor                | ensemble              |                                  | Yes                            |


### XGBoost [[link](https://xgboost.readthedocs.io/en/latest/)]

| Name                           | Package               | Direct transpile (at 21-02-2020) | ONNX transpile (sometime 2020) |
| :----------------------------- | :-------------------- | -------------------------------- | :----------------------------- |
| XGBModel                       | XGboost               | Yes                              |                                |
| XGBClassifier                  | XGboost               | Yes                              |                                |
| XGBRegressor                   | XGboost               | Yes                              |                                |
| XGBRFClassifier                | XGboost               | Yes                              |                                |
| XGBRFRegressor                 | XGboost               | Yes                              |                                |

## References:

* We try to stick to [http://google.github.io/styleguide/pyguide.html](http://google.github.io/styleguide/pyguide.html).
* Package structure: [https://packaging.python.org/tutorials/packaging-projects/](https://packaging.python.org/tutorials/packaging-projects/)