import json

# Save the high score to json file
def save_high_score(score):
    d = {"high_score":score}
    json.dump(d, open("high_score.json","w"))

# Load high score from file
def load_high_score():
    try: 
      d = json.load(open("high_score.json"))
      if "high_score" in d:
          return d["high_score"]
    except:
        pass
    
    return 0