# Compare the benchmarks with the actual results of the LLM models
from tonic_validate import ValidateApi, ValidateScorer, LLMResponse
from tonic_validate.metrics import (
    AnswerConsistencyMetric,
    AnswerSimilarityMetric,
    AugmentationAccuracyMetric,
    AugmentationPrecisionMetric,
    RetrievalPrecisionMetric
)
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

validate_api = ValidateApi(st.secrets["TONIC_VALIDATE_API_KEY"])

benchmarks = {
    "https://www.k12.com/": "4ab8394b-b52b-45a8-b1ad-9a55c85bfcf1"
}

benchmark = validate_api.get_benchmark("4ab8394b-b52b-45a8-b1ad-9a55c85bfcf1")

responses = []

features = {
    "search": False,
    "description": True,
    "highlighting": True,
    "thumbnails": True,
    "filters": True,
    "sorting": True,
    "pagination": False,
    "autocomplete": True
},
for item in benchmark:
    # llm_answer is the answer that LLM gives
    # llm_context_list is a list of the context that the LLM used to answer the question
    print(item.question)

    llm_response = LLMResponse(
        llm_answer=str(features),
        llm_context_list=[str(features)],
        benchmark_item=item
    )
    responses.append(llm_response)

# To see more metric options go to https://github.com/TonicAI/tonic_validate
scorer = ValidateScorer([
    #AnswerConsistencyMetric(),
    AnswerSimilarityMetric(),
    #AugmentationAccuracyMetric(),
    #AugmentationPrecisionMetric(),
    #RetrievalPrecisionMetric()
])
run = scorer.score_run(responses)

validate_api.upload_run(st.secrets["TONIC_VALIDATE_PROJECT_ID"], run)
