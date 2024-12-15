from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

# Load the model and tokenizer from the saved directory
model = AutoModelForSeq2SeqLM.from_pretrained("summarizer_model")
tokenizer = AutoTokenizer.from_pretrained("summarizer_model")

# Initialize the summarization pipeline
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# Test the loaded model
text = "Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to the natural intelligence displayed by humans or animals."
summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
print("Summary:", summary[0]['summary_text'])
