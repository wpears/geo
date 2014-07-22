var fs=require('fs')
  , x = -13544621
  , y = 4613081
  , str = ''
  , xyz=fs.createWriteStream('./fakexyz.txt')
  ;
  xyz.write('x, y, z \n');
for(var z=50; z > -681; z--){
  for(var i = 0; i < 300; i+=3){
    for(var j = 0; j < 15; j+=3){
      str+=(x+i)+', '+(y-j)+', '+(z/10)+' \n';
    }
    xyz.write(str);
    str='';
  }
  y=y-15;
}