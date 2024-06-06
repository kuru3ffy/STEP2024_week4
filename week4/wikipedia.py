import sys
import collections

class Wikipedia:

    # Initialize the graph of pages
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ", 1)
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        start_id = None
        goal_id = None

        # Find the ids for the start and goal pages
        for id, title in self.titles.items():
            if title == start:
                start_id = id
            if title == goal:
                goal_id = id

        if start_id is None or goal_id is None:
            print(f"Either start '{start}' or goal '{goal}' page does not exist.")
            return

        # Breadth-First Search (BFS) to find the shortest path
        queue = collections.deque([(start_id, [start_id])])
        visited = set()

        while queue:
            current_id, path = queue.popleft()

            if current_id == goal_id:
                # Convert path of IDs to path of titles
                shortest_path = [self.titles[id] for id in path]
                print("Shortest path:", " -> ".join(shortest_path))
                return

            if current_id not in visited:
                visited.add(current_id)
                for neighbor in self.links[current_id]:
                    if neighbor not in visited:
                        queue.append((neighbor, path + [neighbor]))

        print(f"No path found from '{start}' to '{goal}'")
    

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self, num_iterations=100, damping_factor=0.85):
        num_pages = len(self.titles)
        page_ranks = {id: 1 / num_pages for id in self.titles}

        for _ in range(num_iterations):
            new_page_ranks = {id: (1 - damping_factor) / num_pages for id in self.titles}

            for id in self.titles:
                linking_pages = self.links[id]
                if linking_pages:
                    distributed_rank = damping_factor * page_ranks[id] / len(linking_pages)
                    for dst in linking_pages:
                        new_page_ranks[dst] += distributed_rank

            page_ranks = new_page_ranks

        # Print the top 10 pages by rank
        sorted_page_ranks = sorted(page_ranks.items(), key=lambda x: x[1], reverse=True)[:10]
        print("The most popular pages are:")
        for id, rank in sorted_page_ranks:
            print(f"{self.titles[id]}: {rank}")

        # Check that the sum of all page ranks is 1
        total_rank = sum(page_ranks.values())
        print(f"Total PageRank: {total_rank}\n")

    # Do something more interesting!!
    def find_something_more_interesting(self):
        # To find the two pages that are the farthest apart, we'll use BFS from each page and measure the distance.
        max_distance = 0
        page_pair = None

        for start_id in self.titles:
            distances = {start_id: 0}
            queue = collections.deque([start_id])

            while queue:
                current_id = queue.popleft()
                current_distance = distances[current_id]

                for neighbor in self.links[current_id]:
                    if neighbor not in distances:
                        distances[neighbor] = current_distance + 1
                        queue.append(neighbor)
                        if distances[neighbor] > max_distance:
                            max_distance = distances[neighbor]
                            page_pair = (start_id, neighbor)

        if page_pair:
            start_page, end_page = self.titles[page_pair[0]], self.titles[page_pair[1]]
            print(f"The farthest pages are '{start_page}' and '{end_page}' with a distance of {max_distance}")
        else:
            print("Could not determine the farthest pages")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("渋谷", "小野妹子")
    wikipedia.find_most_popular_pages()
    wikipedia.find_something_more_interesting()
