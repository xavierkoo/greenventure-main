<template>
  <div class="mission">
    <h1 style="text-align: center">This is Smart Paper Rubbish Bin</h1>
  </div>
  
  <div style="text-align: center; font-size:30px">

    <span>{{ verification_code[0] }}</span>
    <span>{{ verification_code[1] }}</span>
    <span>{{ verification_code[2] }}</span>
    <span>{{ verification_code[3] }}</span>
    <span>{{ verification_code[4] }}</span>
    <span>{{ verification_code[5] }}</span>

    <div>
      <button @click="generate_code()">Generate Code</button>
    </div>

    <img style="padding:20px; width:200px; height:auto" src="../assets/paper_recycling_bin.png" alt="">


  </div>

</template>

<script>  

  import axios from 'axios'
  export default{ 

    data() {
    return {
      category: 'Paper',
      verification_code: '------'
    };
  },
  
  methods: {

    generate_code() {
      // handle redeem confirmation here
      // ...

      let api_endpoint = "http://127.0.0.1:5105/generate_code" 
      console.log(api_endpoint)
      // console.log(user_details.userid)
      axios.post(api_endpoint, { 
        mission_category: this.category, 
      })
      .then(response => {
        
        this.verification_code = response.data.data.verification_code

        console.log(this.verification_code)

      })
      .catch(error => {
          console.log( error.message )
      })

      // for testing purposes to stop regenerating everytime
      // this.verification_code = '111111'

    },
  },
  }

</script>
