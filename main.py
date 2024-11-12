from rankingTool.GUI import GUI

config_file = "rankingTool2.0/config_rest.toml"

def main():
    instance = GUI(config_file)
    instance.show()

if __name__ == "__main__":
    main()
