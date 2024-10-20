from fastapi import FastAPI

app=FastAPI()

class details(str):
    name ="key1"
    name2="key2"
    name3 = "key3"
    name4 = "key4"
    name5 = "key5"

@app.get("/get/{word}")
def main(word):
    if word == details.name:
        return {"message":"Execute plan a"}
    elif word==details.name2:
        return {"message":"Execute plan b"}
    elif word==details.name3:
        return {"message":"Execute plan c"}
    elif word==details.name4:
        return {"message":"Execute plan d"}
    elif word==details.name5:
        return {"message":"Execute plan e"}
    else:
        return {"message":"key mot found"}