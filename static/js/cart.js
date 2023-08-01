let updateBtns =document.getElementById('update-cart')

for(let i =0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function (){
        let productId = this.dataset.product
        let action = this.dataset.action
        console.log('productId:',productId,'action:',action)
    })
}