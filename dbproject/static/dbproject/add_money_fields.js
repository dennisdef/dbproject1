document.addEventListener('DOMContentLoaded', function () {
    let t = 0;
    document.querySelector('#type').addEventListener('change', () => {
        if(t == 0){
            t++;
            let value = document.querySelector('#type').value;
            if (value === 'Company'){
                document.querySelector('#res1').hidden = false;
            }
            if (value === 'University'){
                document.querySelector('#res2').hidden = false;
            }
            if (value === 'Research Center'){
                document.querySelector('#res3').hidden = false;
            }
        } else return;
    });

})