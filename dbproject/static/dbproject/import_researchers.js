document.addEventListener('DOMContentLoaded', function () {
    let times = 0;
    document.querySelector('#organisation').addEventListener('change', () => add_fields()); 
    
    function add_fields(){
            times++;
            var organisation = document.querySelector('#organisation').value;
            var url = '/import_researchers/' + organisation;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    const select = document.createElement('select');
                    const label = document.createElement('label');
                    const button = document.createElement('button');
                    document.querySelector('#researchers').appendChild(label);
                    document.querySelector('#researchers').appendChild(select);
                    document.querySelector('#add_button').appendChild(button);
                    button.setAttribute('class', 'btn btn-outline-danger')
                    button.setAttribute('id', 'add_researcher')
                    button.setAttribute('type', 'button')
                    button.innerHTML = 'Add Researcher';
                    label.innerHTML = 'Researcher';
                    select.setAttribute('id', times);
                    select.setAttribute('name', times);
                    select.setAttribute('class', 'form-control mb-2');
                    select.innerHTML = "";
                    data.forEach(function (researcher) {
                        var option = document.createElement('option');
                        option.value = researcher.id;
                        option.text = researcher.name;
                        select.appendChild(option); 
                    }); 
                    document.querySelector('#add_researcher').addEventListener('click', () => add_researcher());
                });
    }

    

    function add_researcher(){
        times++;
        var organisation = document.querySelector('#organisation').value;
        var url = '/import_researchers/' + organisation;
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    if(times > data.length){
                        alert('No more researchers to add');
                        return;
                    }
                    const select = document.createElement('select');
                    const label = document.createElement('label');
                    document.querySelector('#researchers').appendChild(label);
                    document.querySelector('#researchers').appendChild(select);
                    label.innerHTML = 'Researcher';
                    select.setAttribute('id', times);
                    select.setAttribute('name', times);
                    select.setAttribute('class', 'form-control mb-2');
                    select.innerHTML = "";
                    data.forEach(function (researcher) {
                        var option = document.createElement('option');
                        option.value = researcher.id;
                        option.text = researcher.name;
                        select.appendChild(option); 
                    }); 
                });
    }

})
