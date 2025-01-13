import os

def GraphImageCreator(graph):
    try:
        if os.path.exists("graph.png"):
            print("Image already existed")

        else:
            img = graph.get_graph().draw_mermaid_png()
            with open("graph.png", "wb") as file:
                file.write(img)
            print("Image stored successfully!!!")

    except Exception as e:
        print(e)


if __name__=='__main__':
    from graph_creator import GraphCreator
    graph=GraphCreator()
    GraphImageCreator(graph)
