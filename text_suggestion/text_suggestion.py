import reflex as rx

from rxconfig import config

from utils import clear_message_body, apply_clear_function, load_datasets, cache_data_frame
from features import NGramLanguageModel, PrefixTree, TextSuggestion, WordCompletor
from utils.dataset_utils import get_tokens

# region env

CLEAR = False
DATASET_FILE_NAME = 'cleared_dataset.csv'
N_WORDS = 3
N_TEXTS = 1
N = 3

# endregion

# region loading

print("Loading dataset")
dataset = load_datasets(DATASET_FILE_NAME)

# endregion

# region clearing

if(CLEAR):
    print("Clearing dataset")
    dataset = apply_clear_function(
        data=dataset, 
        data_column='message', 
        clear_func=clear_message_body, 
        drop_columns=['file']
    )
    
    print("Caching dataset")
    cache_data_frame(dataset, 'cleared_dataset.csv')

# endregion

# region corpus tranforms

print(f"Applying corpus transforms")
corpus = get_tokens(dataset, 'message')
corpus = corpus[:1000]

print(f'Corpus size is {len(corpus)}')

# endregion

# region init

print("Initialization")

print("initing WordCompletor")
word_completor = WordCompletor(corpus)
print("initing NGramLanguageModel")
ngram_model = NGramLanguageModel(corpus, N)
print("initing TextSuggestion")
text_seggestion = TextSuggestion(word_completor, ngram_model)

# endregion

class State(rx.State):
    text: str = ""
    predicted: str = ""
    completed_word: str = ""
    
    def reset_state(self):
        self.text = ""
        self.predicted = ""
    
    def on_suggestion_select(self, suggestion):
        print(f"State on_suggestion_select -> suggestion = {suggestion}")
        
        self.text = self.text.strip() + ' ' + suggestion + ' '
        
        self.predicted = ''
          
    def on_completed_word_select(self):
        words = self.text.strip().split()
        self.text = ' '.join(words[:-1] + [self.completed_word])
        self.completed_word = ''
    
    def on_change(self, text):
        print(f"\nState: on_change -> text = {text}")
        self.text = text
        words = text.strip().split()
        
        if(len(words) == 0):
            return self.reset_state()
        
        last_word = words[-1]
        
        print(f"State: on_change -> last_word = {last_word}")
        
        completions, probs = word_completor.get_words_and_probs(last_word)
    
        if completions:
            completed_word = completions[probs.index(max(probs))]
            print(f"State: on_change -> completed_word = {completed_word}")
            # self.text = ' '.join(words[:-1] + [completed_word])
            self.completed_word = completed_word
        else:
            print(f"State: on_change -> no completions")
            # self.text = self.text
            self.completed_word = ''
            
        predicted = text_seggestion.suggest_text(words, n_words=N_WORDS, n_texts=N_TEXTS)
        print(f"State: on_change -> predicted = {predicted}")
        self.predicted = ' '.join(predicted[0][len(words):]) if predicted else ''

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Text Suggestion", size="9"),
            rx.text_area(
                placeholder="Write something…",
                value=State.text,
                on_change=State.on_change,
                size="3"
            ),
            rx.cond(
                State.completed_word == '',
                rx.text("Here will be word completions..."),
                rx.button(
                    State.completed_word,
                    on_click=State.on_completed_word_select,
                    size="3",
                    variant="soft",
                    color_scheme="grass",
                    disabled=State.completed_word == ''
                ),
            ),
            rx.text_area(
                placeholder="Here will be predicted text…",
                value=State.predicted,
                disabled=True,
                size="3"
            ),
            rx.button(
                'Add prediction to text',
                on_click=lambda: State.on_suggestion_select(State.predicted),
                size="3",
                variant="soft",
                color_scheme="grass",
                disabled=State.predicted == ''
            ),
            
            spacing="5",
            justify="center",
            min_height="85vh",
            min_width="60wv"
        ),
    )


app = rx.App()
app.add_page(index)
