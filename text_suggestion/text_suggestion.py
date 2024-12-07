import reflex as rx

from rxconfig import config

from utils import clear_message_body, apply_clear_function, load_datasets, cache_data_frame
from features import NGramLanguageModel, PrefixTree, TextSuggestion, WordCompletor

# eegion env

CLEAR = False
DATASET_FILE_NAME = 'cleared_dataset.csv'

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

print("Getting corpus")
corpus =  [word for sublist in dataset for word in sublist]

# endregion

# region init

print("Initialization")
word_completor = WordCompletor(corpus)
ngram_model = NGramLanguageModel(corpus, 5)
text_seggestion = TextSuggestion(word_completor, ngram_model)

# endregion

class State(rx.State):
    """The app state."""

    ...


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Welcome to Reflex!", size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.link(
                rx.button("Check out our docs!"),
                href="https://reflex.dev/docs/getting-started/introduction/",
                is_external=True,
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )


app = rx.App()
app.add_page(index)
