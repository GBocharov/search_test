from typing import Union, List

from text_utils.text_cleaners.cleaning import ru_embedding_clean


class CleaningFunction:
    def __call__(self, input_str: Union[str, List[str]]) -> Union[str, List[str]]:
        ...


class NoCleanFunction(CleaningFunction):
    def __call__(self, input_str: Union[str, List[str]]) -> Union[str, List[str]]:
        return input_str


class SimpleCleanFunction(CleaningFunction):
    def __call__(self, input_str: Union[str, List[str]]) -> Union[str, List[str]]:
        is_input_was_string = False
        if isinstance(input_str, str) or not hasattr(input_str, '__len__'):
            input_str = [input_str]
            is_input_was_string = True

        cleaned_strs = [ru_embedding_clean(item) for item in input_str]
        if is_input_was_string:
            return cleaned_strs[0]
        return cleaned_strs


text_cleaning_f = SimpleCleanFunction()

if __name__ == '__main__':
    cleaner = SimpleCleanFunction()
    text = r"Какой-то текст     говды   ызвы выв ы   12 12 12  333   "
    texts = ['sdas', 'asdf', 'sadas']
    print(cleaner(1))
