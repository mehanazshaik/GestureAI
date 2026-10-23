class FilterManager:

    def __init__(self):

        # Available filters
        self.filters = [
            "Paris",
            "Oslo",
            "Tokyo",
            "Seoul"
        ]

        # Start with first filter
        self.current_index = 0

    def next_filter(self):

        self.current_index += 1

        # Go back to first filter
        if self.current_index >= len(self.filters):
            self.current_index = 0

        return self.get_current_filter()

    def previous_filter(self):

        self.current_index -= 1

        # Go to last filter
        if self.current_index < 0:
            self.current_index = len(self.filters) - 1

        return self.get_current_filter()

    def get_current_filter(self):

        return self.filters[self.current_index]