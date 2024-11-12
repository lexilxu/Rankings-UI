
from rankingTool.GUI import GUI

#other_paths = {
#    "OS": "Restaurants_Example/OS Ratings.csv",
#    "FQ": "Restaurants_Example/FQ Ratings.csv",
#    "ST": "Restaurants_Example/ST Ratings.csv",
#    "WS": "Restaurants_Example/WS Ratings.csv",
#    "MK": "Restaurants_Example/MK Ratings.csv"
#}
#ranking_path = "Restaurants_Example/Ranking.csv"
#OP_path = "Restaurants_Example/OP_new.csv"
#reviews_path ="Restaurants_Example/Reviews.csv"
config_file = "config_rest.toml"

mod_attributes = {'Mallows': dict(),
                  'RIM': dict(iters=100, temp=.03),
                  'GMM': dict(),
                  'Landmarks': dict(),
                  'Borda':dict()}

#ratings, props, reviewers, reviews, rest_names = distr_df(ranking_path, OP_path, other_paths, reviews_path)
#res, tie = rankings(ranking_path)
#ranks = Rankings(ratings, res, tie, rating_names=list(ratings.columns[:6]), overall_col_name="OP")
#reviewers = Reviewers(reviewers)
#reviews = Reviews(reviews, ["One-word Rating"])
#props = Proposals(props)
#rankings_path = "Restaurants_Example/restaurants_clean.txt"

rest_names = {"short": ["Chip","MMF", "UDF", "Costa", "Thai", "Palmi", "CM", "TofX", "JB", "K Tofu", "SK", "PS"],
              "long": ['Chipotle',
                       'Memos Mexican F',
                       'U:Don Fresh Jap',
                       "Costa's Restaur",
                       'Thai Tom',
                       'Palmi Korean BB',
                       'Chi Mac',
                       "Taste of Xi'an",
                       'Just Burgers',
                       'Korean Tofu Hou',
                       'Shawarma King',
                       'Pho Shizzle']
}

def main():
    instance = GUI(config_file)
    instance.show()


if __name__ == "__main__":
    main()
