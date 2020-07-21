window.addEventListener('DOMContentLoaded', event => {
    console.log('loaded')
    document.querySelector('#save-tag').addEventListener('click', () => {
        console.log('saved')
        $('#tagModal').modal('hide');
    })
})
