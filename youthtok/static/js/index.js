//-------------------------for gallery
//--------------------

//notifications
const menuitems = document.querySelectorAll('.menu-items');
//messages

//theme
const theme = document.querySelector('#theme')
const thememodal = document.querySelector('.customized-theme')
const fontsizes = document.querySelectorAll('.choose-size, span')
var root = document.querySelector(':root');
const colorplate = document.querySelectorAll('.choose-color span')
const bg1 = document.querySelector('.bg-1')
const bg2 = document.querySelector('.bg-2')
const bg3 = document.querySelector('.bg-3')

const changeactiveitems = () => {
    menuitems.forEach(item => {
        item.classList.remove('active');
    })
}


menuitems.forEach(item => {
    item.addEventListener('click', () => {
        changeactiveitems();
        item.classList.add('active');
        if(item.id != 'notifications'){
            document.querySelector('.notifications-popup').
            style.display = 'none';
            
        } else{
            document.querySelector('.notifications-popup').
            style.display = 'block';
            document.querySelector('#notifications .notifications-count').
            style.display = 'none';
        }
    })
})

//search chat
////////////////////////////////////////////
//const searchmessage = () => {
  //  const val = messagesearch.value.toLowerCase();
    //message.forEach(user => {
      //  let name = user.querySelectorAll('h5').textContent.toLowerCase();
        //if(name.indexOf(val) != 1){
          //  user.style.display = 'flex';
  //      } else{
    //        user.style.display = 'none';
      //  }
//    })
//}
// messagesearch.addEventListener('keyup', searchmessage);
////////////////////////////////////////////////////////

//// theme display cust
const openthememodal = () => {
    thememodal.
    style.display = 'grid'
}
const closethememodal = (e) => {
    if(e.target.classList.contains('customized-theme')){
        thememodal.style.display = 'none'
    }
} 

thememodal.addEventListener('click', closethememodal);

theme.addEventListener("click", openthememodal)


const removesizeselector = () => {
    fontsizes.forEach(size => {
        size.classList.remove('active');
    })
}
////fonts
fontsizes.forEach(size => {
    size.addEventListener('click', () => {
    let font;
    size.classList.toggle('active');
        if(size.classList.contains('font-size-1')){
            font = '10px';
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '5.4rem');
        } else if(size.classList.contains('font-size-2')){
            font = '13px';
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '-7rem');
        } else if(size.classList.contains('font-size-3')){
            font = '16px';
            root.style.setProperty('----sticky-top-left', '2rem');
            root.style.setProperty('----sticky-top-right', '-17rem');
        } else if(size.classList.contains('font-size-4')){
            font = '19px';
            root.style.setProperty('----sticky-top-left', '-5rem');
            root.style.setProperty('----sticky-top-right', '-25rem');
        } else if(size.classList.contains('font-size-5')){
            font = '22px';
            root.style.setProperty('----sticky-top-left', '-10rem');
            root.style.setProperty('----sticky-top-right', '-33rem');
        }

        ////change html fonts
    document.querySelector('html').style.fontSize = font;
    })
})

//color 
const changecolor = () => {
    colorplate.forEach(colorplate => {
        colorpiker.classList.remove('active')
    })
}

colorplate.forEach(color => {
    color.addEventListener('click', () => {
        let primary;
        changecolor
        if(color.classList.contains('color-1')){
            primaryhue = 251;
        } else if(color.classList.contains('color-2')){
            primaryhue = 52;
        } else if(color.classList.contains('color-3')){
            primaryhue = 332;
        } else if(color.classList.contains('color-4')){
            primaryhue = 152;
        } else if(color.classList.contains('color-5')){
            primaryhue = 202;
        }
        color.classList.add('active');
        root.style.setProperty('--primary-color-hue', primaryhue);
    })
})


//background
let lightcolorlightness;
let whitecolorlightness;
let darkcolorlightness;

const changeBG = () => {
    root.style.setProperty('--light-color-lightness', lightcolorlightness);
    root.style.setProperty('--white-color-lightness', whitecolorlightness);
    root.style.setProperty('--dark-color-lightness', darkcolorlightness);
}
bg1.addEventListener('click', () => {
    //add active
    bg1.classList.add('active');
    bg2.classList.remove('active');
    window.Location.reload();
    changeBG();
})

bg2.addEventListener('click', () => {
    darkcolorlightness = '95%';
    whitecolorlightness = '20%';
    lightcolorlightness = '15%';

    //add active
    bg2.classList.add('active');
    bg1.classList.remove('active');
    changeBG();
})





/////////////////////////////comment toggle for post&comments.html//////

function commentreplytoggle(parent_id){
    const row = document.getElementById(parent_id);

    if (row.classList.contains('d-none')){
        row.classList.remove('d-none');
    }else{
        row.classList.add('d-none');
    }
}
