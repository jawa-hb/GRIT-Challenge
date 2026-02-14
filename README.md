\# Codeforces Temporal Rating Prediction Challenge



This repository contains the Codeforces Temporal Rating Prediction Challenge — a benchmark designed to evaluate graph‑based models on the task of predicting competitive programmer rating evolution on a dynamic homogeneous graph.



Participants will develop models that take \*\*historical user and contest information\*\* and \*\*graph structure\*\* as input, and output predictions for user ratings at their next contest participation.



---



\## 🧠 Overview



Competitive programming platforms such as Codeforces provide rich longitudinal data reflecting how participants’ skills evolve over time. We formulate this evolution as a \*\*dynamic homogeneous graph problem\*\* where:



\- Nodes represent users at specific contests

\- Edges capture temporal continuity and competitive proximity

\- Models must operate in an \*\*autoregressive setting\*\*, predicting future ratings based only on past and present information



This challenge encourages research into temporal message passing, autoregressive reasoning, and robust prediction under evolving graph structure.



---



\## 📦 Data



The dataset is organized into training and test splits, each representing \*\*events over time\*\*. Each row corresponds to a user’s participation in a contest.



\### Node representation



Each node corresponds to: 



(user\_id, contest\_id)



and includes features known at the end of contest \\( t \\):



| Feature                      | Description |

|-----------------------------|-------------|

| `old\_rating`                | Rating before contest \\(t\\) |

| `rating`                   | Rating after contest \\(t\\) |

| `num\_problems\_solved`      | Number of problems solved in contest \\(t\\) |

| `problems\_solved`          | Representation of the specific problems solved |

| `participation\_gap`        | Number of contests since last participation |

| `contest\_participant\_count`| Official number of participants in contest \\(t\\) |



\*\*Important:\*\* Participants should not use future ratings beyond the current input.



---



\## 🔗 Graph Construction



The graph evolves across contests and contains two edge modalities:



\### Temporal edges



For each user, connect their participation nodes chronologically:



(node at contest t) → (node at contest t')



where \\( t' \\) is the next contest this user appears in.



These edges allow models to pass user‑specific historical information forward.



---



\### Neighborhood edges



Within the same contest snapshot, connect users whose starting rating (old\_rating) is similar:



(u\_i, t) — (u\_j, t) if |old\_rating\_i − old\_rating\_j| ≤ δ



These \*peer similarity edges\* encode competitive proximity.



---



\## 🎯 Prediction Task



Your model must, for each node in the test set, produce:



next\_rating



This is the rating of the user at their next contest participation, which is not present in the test features.



\#### Autoregressive protocol



\- The model predicts ratings sequentially.

\- For multiple test contests for the same user, the model should use its own previous predictions as input (`old\_rating`) for later steps.

\- True labels of future test events must not be used during prediction.



---



\## 📊 Evaluation



Predictions are assessed with the following metrics:



\### Primary metric



\*\*Mean Absolute Error (MAE)\*\* between predicted and true ratings:



\\\[

\\text{MAE} = \\frac{1}{N} \\sum\_{i=1}^N | \\hat{y}\_i - y\_i |

\\]



This is the \*\*official ranking metric\*\* on the leaderboard.



---



\### Secondary metric



\*\*Root Mean Squared Error (RMSE)\*\*:



\\\[

\\text{RMSE} = \\sqrt{\\frac{1}{N} \\sum\_{i=1}^N (\\hat{y}\_i - y\_i)^2}

\\]



RMSE is \*\*reported\*\* as an additional measure of prediction stability and to help distinguish models with similar MAE.



---



\### Diagnostic metrics (not on leaderboard)



The following may be useful for model analysis:



\- Step‑ahead error curves (e.g., MAE at 1–5 steps ahead)

\- Directional accuracy (predicting up/down correctly)

\- Error drift over long sequences



---



\## 🖇 Submission Format



Your submission must be a CSV with two columns:



```csv

node\_id,predicted\_next\_rating



* node\_id refers to the test node identifier



* predicted\_next\_rating is your model’s forecast of that user’s next rating



Predictions should be in the same order as test.csv.



📜 Rules



No external Codeforces data: Do not incorporate additional Codeforces data not provided in this dataset.



Autoregressive only: Models must run in a sequential prediction setting; use their own predictions as inputs for future test steps.



No peeking at future labels: Participants must not use true future ratings from test nodes.



No handcrafted heuristics exploiting hidden information. Models should learn from the provided structure and features.















