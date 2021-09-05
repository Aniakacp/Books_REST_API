document.addEventListener("DOMContentLoaded",function(event){
    console.log('sdkfidsuhfs')
    fetch('https://www.googleapis.com/books/v1/volumes?q=Hobbit')
    .then(response=>{
        if(response.ok){return response.json()}
        else{return Promise.reject("Error"+response.status)}
    })
    .then(response=>{
        let whereToAdd = document.getElementsByClassName('list')[0]
            console.log(whereToAdd)
        for (let i = 0; i < response.items.length; i++) {

        const new_title = document.createElement("li");
            new_title.innerText = response.items[i].volumeInfo.title
            whereToAdd.appendChild(new_title)
        let authors= response.items[i].volumeInfo.authors
            console.log(authors, 'authors')
        let published_date= response.items[i].volumeInfo.publishedDate
            console.log(published_date, 'date')
        let categories= response.items[i].volumeInfo.categories
            console.log(categories, 'cat')
        let average_rating= response.items[i].volumeInfo.averageRating
            if(average_rating){
                console.log(average_rating, 'avg rating')
            }
        let ratings_count= response.items[i].volumeInfo.ratingsCount
            if(ratings_count)
            {console.log(ratings_count, 'ratings count')}

        let thumbnail= response.items[i].volumeInfo.imageLinks
            if (thumbnail){
            console.log(Object.entries(thumbnail)[1][1], 'thumbnail')
            }
        }
        
    })
    .catch(function(err) {
        console.log(err)})
    
    })