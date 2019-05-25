

def callHEREMAPS(location1, location2):
    mapsweb = webbrowser.open_new("https://tkchui.github.io/algomap/map1.html?path=" + str(location1) + "," + str(location2))


callHEREMAPS("Australia", "United States")