document.addEventListener('DOMContentLoaded', function () {
    let times = 0;
    let organisation = 0;
    document.querySelector('#organisation').addEventListener('change', () => add_fields()); 
    function add_fields(){
            if(times == 0){
                times++;
                organisation = document.querySelector('#organisation').value;
                var url = '/import_researchers/' + organisation;
                fetch(url)
                    .then(response => response.json())
                    .then(data => {
                        const select = document.querySelector('#lead_researcher');
                        document.querySelector('#res').hidden = false;
                        data.forEach(function (researcher) {
                            var option = document.createElement('option');
                            option.value = researcher.id;
                            option.text = researcher.name;
                            select.appendChild(option); 
                        }); 
                        const select2 = document.querySelector('#researchers');
                        data.forEach(function (researcher) {
                            var option = document.createElement('option');
                            option.value = researcher.id;
                            option.text = researcher.name;
                            select2.appendChild(option);
                        });
                    })
            }else return;
    }
})
