var arr = [1,3,4,23,"hey",{},true];

// foreach map filter find indexOf


//apply to all members of array
arr.forEach(function (val){
    console.log(val + " hello");
});

// make another blank array -- map (return a new array having equal no. of elements to arr)

var newArr = arr.map(function (val){
    return 13;
})

console.log(newArr);

var filArr = arr.filter(function (val){
    if(val>3){
        return true;
    }
    else return false;
})

console.log(filArr);


var res = arr.find(function (val) {
    if(val==23) return val;
})
// present -- return | undefined (not present)

console.log(res);

// Object

var obj={
    name:"VA"
}

console.log(obj.name)
console.log(obj["name"])
// Object.freeze(obj) ---- cannot change

// ---------
// function length

// function.length --- object -- contains property -> length

// ASYNC JS --

// var blob = await fetch(`https://randomuser.me/api/`);
// var res = await blob.json();

// console.log(blob);

// ---Line by line code is running---

// async nature 
// usey side stack mai snd kr do and next code ko run kro jo sync nature ka ho 
// and jb bhi sb sync code run hojae -- main stack khali hojae tb check kro async
// code complete hua ya nhi agr vo complete hua ho toh usey main stack mai laao and chla do 

async function abcd(){
var blob = await fetch(`https://randomuser.me/api/`);
var ans = await blob.json();
console.log(ans.results[0].name);
}

abcd();
