def main():
    print ''
    print "RUNNING SNIPPET = MATTE CLEANER"
    print "A mini toolkit to cleanup crap around a more solid matte without having to garbage mask."
    print "Could also be used to remove or isolate different sizes of floating particles."
    print "Extend the principle to your liking ..."

    import flame

    selected = flame.batch.current_node.get_value()
    # print selected.attributes

    mux_in = flame.batch.create_node("Mux")
    mux_in.name = "cleanMatte_IN"
    mux_in.pos_x = selected.pos_x + 250
    mux_in.pos_y = selected.pos_y

    matte_edge1 = flame.batch.create_node("Matte Edge")
    matte_edge1.name = "shrink"
    matte_edge1.pos_x = mux_in.pos_x + 100
    matte_edge1.pos_y = mux_in.pos_y - 150
    matte_edge1.load_node_setup("/opt/flame_dev/house_projects/17P998_python_console/devl/snippets_setups/edge/shrink_4.edge_node")

    matte_edge2 = flame.batch.create_node("Matte Edge")
    matte_edge2.name = "expand"
    matte_edge2.pos_x = matte_edge1.pos_x + 200
    matte_edge2.pos_y = matte_edge1.pos_y + 0
    matte_edge2.load_node_setup("/opt/flame_dev/house_projects/17P998_python_console/devl/snippets_setups/edge/expand_4.edge_node")

    comp1 = flame.batch.create_node("Comp")
    comp1.name = "clean_around"
    comp1.pos_x = matte_edge2.pos_x + 100
    comp1.pos_y = matte_edge1.pos_y + 150

    flame.batch.connect_nodes(selected, "Default", mux_in, "Default")
    flame.batch.connect_nodes(mux_in, "Default", matte_edge1, "Default")
    flame.batch.connect_nodes(matte_edge1, "Default", matte_edge2, "Default")
    flame.batch.connect_nodes(mux_in, "Default", comp1, "Front")
    flame.batch.connect_nodes(matte_edge1, "Default", comp1, "Back")
    flame.batch.connect_nodes(matte_edge2, "Default", comp1, "Matte")
