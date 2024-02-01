class SearchAndSort:
    def __init__(self, treeview):
        self.treeview = treeview

    def search(self, query):
        visible_items = []
        for item in self.treeview.get_children():
            if query.lower() in "|".join(self.treeview.item(item, 'values')).lower():
                visible_items.append(item)
        # This example shows all items; you might want to adjust visibility based on the search
        return visible_items

    def sort(self, sort_by):
        all_tracks = [(self.treeview.item(item, 'values'), item) for item in self.treeview.get_children()]
        if sort_by in ["Artist", "Album", "Genre", "Year", "Title"]:
            # Adjust index based on your columns (e.g., 2 for Artist assuming it's the third column)
            sort_index = {"Artist": 2, "Album": 3, "Genre": 4, "Year": 5, "Title": 1}[sort_by]
            sorted_tracks = sorted(all_tracks, key=lambda x: x[0][sort_index])

            for track in sorted_tracks:
                self.treeview.move(track[1], '', 'end')
