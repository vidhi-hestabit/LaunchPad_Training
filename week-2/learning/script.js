function changeText(){
    document.getElementById('fpara');
    fpara.textContent='VA';
}

let fpara=document.getElementById('fpara');
fpara.addEventListener('click', changeText);

let anchorElement=document.getElementById('anchor');

anchorElement.addEventListener('click', function(event){
    event.preventDefault();
    console.log('Default prevented');
});

