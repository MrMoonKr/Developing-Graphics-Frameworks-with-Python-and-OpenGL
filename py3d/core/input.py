class Input:
    def __init__(self):
        # Has the user quit the application?
        self._quit = False
        # lists to store key states
        # down, up: discrete event; lasts for one iteration
        # pressed: continuous event, between down and up events
        self._key_down_list = []
        self._key_pressed_list = []
        self._key_up_list = []
        # queues filled by windowing callbacks; consumed once per frame
        self._pending_key_down_list = []
        self._pending_key_up_list = []

    @property
    def key_down_list(self):
        return self._key_down_list

    @property
    def key_pressed_list(self):
        return self._key_pressed_list

    @property
    def key_up_list(self):
        return self._key_up_list

    @property
    def quit(self):
        return self._quit

    # functions to check key states
    def is_key_down(self, key_code):
        return key_code in self._key_down_list

    def is_key_pressed(self, key_code):
        return key_code in self._key_pressed_list

    def is_key_up(self, key_code):
        return key_code in self._key_up_list

    def set_quit(self, value=True):
        self._quit = bool(value)

    def register_key_down(self, key_name):
        if key_name is None:
            return
        if key_name not in self._key_pressed_list:
            self._key_pressed_list.append(key_name)
            self._pending_key_down_list.append(key_name)

    def register_key_up(self, key_name):
        if key_name is None:
            return
        if key_name in self._key_pressed_list:
            self._key_pressed_list.remove(key_name)
        if key_name not in self._pending_key_up_list:
            self._pending_key_up_list.append(key_name)

    def update(self):
        # Convert callback queues to per-frame snapshots.
        self._key_down_list = self._pending_key_down_list
        self._key_up_list = self._pending_key_up_list
        self._pending_key_down_list = []
        self._pending_key_up_list = []
