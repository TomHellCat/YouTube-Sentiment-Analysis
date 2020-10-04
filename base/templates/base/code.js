let url = 'http://127.0.0.1:8000/thing/';

     const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
    "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"
    ]

     var per_bool = false
     var loc_bool = false
     var org_bool = false
     var misc_bool = false
     var untagged_bool = false
     var enabled_color = "#2962ff"
     var disabled_color = "#e0f2f1"
     var button_class_name = "waves-effect waves-light btn-small"
     var someArray = new Array()
     var uniqueArray = new Array()
    
    var respon
    
    fetch(url)
    .then((resp)=>resp.json())
    .then((data)=>{
        respon = data
        var date = new Array()
        if(data.length > 1){
            modifyData(data,'LOC',5,5)
            modifyData(data,'ORG',15,15)
            modifyData(data,'MISC',40,5)

            for(i=0;i<data.length;i++){
                data[i]['date'] = new Date(data[i]['date'])
                someArray.push(data[i]['tag'])
            }

            //firstSentance("Andrew Yang", 443434354)
            let uniqueSet = new Set(someArray) 
            uniqueSet.delete("")
            //uniqueSet.delete("LOC")
            uniqueSet.delete("PER")
            uniqueArray = Array.from(uniqueSet)
            uniqueArray.push("")
            console.log(uniqueArray)
            
           
           if(uniqueArray.length > 0){
                let tagDiv = document.getElementById("tags")
                let title = document.createElement("button")
                title.className = button_class_name
                title.textContent = uniqueArray.length.toString() + " tags found"

                
                let linebreak = document.createElement("br")
                let linebreak2 = document.createElement("br")
                tagDiv.appendChild(title)
                tagDiv.appendChild(linebreak)
                tagDiv.appendChild(linebreak2)
                for(i=0;i<uniqueArray.length;i++){
                    let btn = document.createElement("button")
                    btn.className = button_class_name
                    btn.textContent = uniqueArray[i]
                    btn.style.marginRight = "40px"
                    btn.style.backgroundColor = enabled_color
                    tagDiv.appendChild(btn)
                    if(uniqueArray[i] == 'PER'){
                        btn.id = "PER"                
                        btn.addEventListener('click',function(){
                            changeColor("PER",data)
                        })
                    }else if(uniqueArray[i] == 'LOC'){
                        btn.id = "LOC"                
                        btn.addEventListener('click',function(){
                            changeColor("LOC",data)
                        })
                    }else if(uniqueArray[i] == 'ORG'){
                        btn.id = "ORG"                
                        btn.addEventListener('click',function(){
                            changeColor("ORG",data)
                        })
                    }else if(uniqueArray[i] == 'MISC'){
                        btn.id = "MISC"                
                        btn.addEventListener('click',function(){
                            changeColor("MISC",data)
                        })
                    }else{
                        btn.id = "UNTAGGED"
                        btn.textContent = "UNTAGGED"
                        btn.addEventListener('click',function(){
                            changeColor("UNTAGGED",data)
                        })
                    }
                }         
           }
            data.sort(function(a, b){
                return a.date - b.date
            })
            console.table(data)
            putItAllTogether(data,uniqueArray)
        }    
    })

    function firstSentance(views,search_term){
        let div = document.getElementById("first_div")
        div.appendChild(document.createElement("span").textContent="Videos mentioning  ")
        let s = document.createElement("strong").textContent = search_term
        s.style.fontSize = 200
        div.appendChild(s)
        div.appendChild(document.createElement("span").textContent=" has over ")
        let v = document.createElement("strong").textContent = views.toString()
        v.style.fontSize = 200
        div.appendChild(v)
        div.appendChild(document.createElement("span").textContent=" views")
    
}

    function modifyData(jsonobjectList, tag,index,number){
        if(index+number < jsonobjectList.length)
            for(i=index;i<index+number;i++)
                jsonobjectList[i]['tag'] = tag
    }


    function addTag(tag){
        if(tag == "UNTAGGED")
            uniqueArray.push("")
        else
            uniqueArray.push(tag)
        console.log(uniqueArray)
    }
   
    function removeTag(tag){
        if(tag == "UNTAGGED")
            tag = ""
        const index = uniqueArray.indexOf(tag)
        if(index > -1)
            uniqueArray.splice(uniqueArray.indexOf(tag),1)
        console.log(uniqueArray)
    }

    function changeColor(tag,data){       
        but = document.getElementById(tag)
        if(tag == "PER"){
            if(per_bool == false){
                if(uniqueArray.length > 1){
                    but.style.backgroundColor = disabled_color
                    per_bool = true
                
                    removeTag(tag)
                    putItAllTogether(data,uniqueArray)
                }      
            }else{
                per_bool = false
                but.style.backgroundColor = enabled_color
                addTag(tag)
                putItAllTogether(data,uniqueArray)
            }
        }else if(tag == "LOC"){
            if(loc_bool == false){
                if(uniqueArray.length > 1){
                    but.style.backgroundColor = disabled_color
                    loc_bool = true
                
                    removeTag(tag)
                    putItAllTogether(data,uniqueArray)
                }
            }else{
                loc_bool = false
                but.style.backgroundColor = enabled_color
                addTag(tag)
                putItAllTogether(data,uniqueArray)
            }
        }else if(tag == "ORG"){
            if(org_bool == false){
                if(uniqueArray.length > 1){
                    but.style.backgroundColor = disabled_color
                    org_bool = true
                    removeTag(tag)
                    putItAllTogether(data,uniqueArray)
                }
            }else{
                org_bool = false
                but.style.backgroundColor = enabled_color
                addTag(tag)
                putItAllTogether(data,uniqueArray)
            }
        }else if(tag == "MISC"){
            if(misc_bool == false){
                if(uniqueArray.length > 1){
                    but.style.backgroundColor = disabled_color
                    misc_bool = true
                
                    removeTag(tag)
                    putItAllTogether(data,uniqueArray)
                }
            }else{
                misc_bool = false
                but.style.backgroundColor = enabled_color
                addTag(tag)
                putItAllTogether(data,uniqueArray)
            }
        }else{
            if(untagged_bool == false){
               if(uniqueArray.length > 1){
                    but.style.backgroundColor = disabled_color
                    untagged_bool = true
                    removeTag(tag)
                    putItAllTogether(data,uniqueArray)
                }
            }else{
                untagged_bool = false
                but.style.backgroundColor = enabled_color

                addTag(tag)
                putItAllTogether(data,uniqueArray)
            }
        }
        
    }
    function getData(data,uniqueArray){
        dataList = new Array()
        for(i=0;i<data.length;i++){
            if(uniqueArray.includes(data[i]['tag'])){
                dataList.push(data[i])
            }
        }
        return dataList
    }

    function modifyChart(tag,data){

    }
    function getStatistics(data){
        var views_p=0
        var views_n=0
        var likes_p=0
        var dislikes_p=0
        var likes_n=0
        var dislikes_n=0

        for(i=0;i<data.length;i++){
            if(data[i]['sentiment'] == true){
                views_p += data[i]['views']
                likes_p += data[i]['likes']
                dislikes_p += data[i]['dislikes']
            }else{
                views_n += data[i]['views']
                likes_n += data[i]['likes']
                dislikes_n += data[i]['dislikes']
            }
        }
        return [views_p, views_n, likes_p,dislikes_p,likes_n,dislikes_n]
    }

    function getMonthList(data){
        let len = data.length-1
        let date = new Array()
        let start = new Date(data[0].date.getFullYear(),data[0].date.getMonth())
        let end = new Date(data[len].date.getFullYear(),data[len].date.getMonth())

        while(start < end){
            let d = new Date(start.getFullYear(),start.getMonth())
            date.push(d)
            start.setMonth(start.getMonth()+1)
        }
        date.push(start)
        return date
    }
    function getYAxis(data,date){
        var i = 0
        var j = 0
        var lastpos = 0
        var count = 0

        let y1 = new Array(date.length).fill(0)
        let y2 = new Array(date.length).fill(0)
        let y = new Array(date.length).fill(0)

        for(i=0;i<data.length;i++){
            for(j=lastpos;j<date.length;j++){
                n_date = new Date(data[i].date.getFullYear(),data[i].date.getMonth())
                if(+date[j] == +n_date){
                    y[j]++
                    lastpos = j
                    if(data[i].sentiment == true){
                        //console.log(true)
                        y1[j]++
                    }else{
                        y2[j]++
                    }
                    break
                }
            }
        }
        return [y1,y2,y]
    }

    function getShorterMonthNames(date){
        for(i=0;i<date.length;i++)
            date[i] = date[i].getFullYear().toString() + " " + monthNames[date[i].getMonth()]
        return date
    }

	function get_shrink_factor(length,no_of_data_points){
			console.log(length);
			var x = 0;
			//console.log(no_of_data_points);
			if(length > no_of_data_points){
				x = Math.round(length/no_of_data_points);
				//console.log(x);
				if(x < length/no_of_data_points){
					x += 1;
					//console.log(length/no_of_data_points);
				}
			}
      else{
        //console.log("x is still zero");
        x = 1
      }
			//console.log(x);
			return x;

	}
	
	function shrink(m,y1,y2,shrink_factor){
		new_m = [];
		new_y1 = [];
		new_y2 = [];
        let last = m[m.length-1]

		for(i=0;i<m.length;){
			new_m.push(m[i]);
			j = i;
			y1_el = 0;
			y2_el = 0;
			i = i+shrink_factor
			for(;j<i;j++){
				if(j > m.length-1)
					break;
				y1_el += y1[j];
				y2_el += y2[j];
			}
			new_y1.push(y1_el);
			new_y2.push(y2_el);
		}
        new_m[new_m.length-1] = last
		return [new_m,new_y1,new_y2];
	}

    function drawChart(date,y1,y2,y){
        var ctx = document.getElementById('myChart').getContext('2d');
        var chart = new Chart(ctx, {
        // The type of chart we want to create
            type: 'line',
            data: {
                labels: date,
                datasets: [{
                    label: 'All Videos',
                    backgroundColor: 'rgba(255, 99, 132,0)',
                    borderColor: 'rgb(0, 0, 255)',
                    data:y
                },
                {
                    label: 'Unfavourable Videos',
                    backgroundColor: 'rgba(255, 99, 132,0)',
                    borderColor: 'rgb(255, 0, 0)',
                    data:y2
                },
                {
                    label: 'Favourable Videos',
                    backgroundColor: 'rgba(255, 99, 132,0)',
                    borderColor: 'rgb(0, 255, 0)',
                    data:y1
                }
                ]
            },

            // Configuration options go here
            options: {
                legend: {
                    display: true,
                    labels: {
                        fontColor: 'rgb(255, 99, 132)',
                        padding: 150
                    }
                },
                 tooltips: {
                    backgroundColor:'rbga(0,0,0,0)',
                    titleFontColor:'rgb(0,0,0)',
                    bodyFontColor: 'rgb(0,0,0)'
                    }
            }
        })
    }
    function putItAllTogether(data,uniqueArray){
        var new_data = getData(data,uniqueArray)
        date = getMonthList(new_data)
        console.log(date)
        var y = new Array()
        var y1 = new Array()
        var y2 = new Array()
        let new_array = getYAxis(new_data,date)
        y1 = new_array[0]
        y2 = new_array[1]
        y = new_array[2]
        date = getShorterMonthNames(date)
        shrink_factor = 1;
        shrink_factor = get_shrink_factor(date.length,17);
        list = shrink(date,y1,y2,shrink_factor);
        date = list[0];
        y1 = list[1];
        y2 = list[2];
        drawChart(date,y1,y2,y)
    }