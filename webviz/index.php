<!DOCTYPE html>
<meta charset="utf-8">
<!-- load the d3.js library -->    
<script type="text/javascript" src="lib/d3/d3.v3.js"></script>
<script type="text/javascript" src="js/doVizC.js"></script>
<script type="text/javascript" >
  function preloadData(val) {
    loadData(val);
  }

</script>
<style> /* set the CSS */

body { font: 12px Arial;}

path { 
    stroke: steelblue;
    stroke-width: 2;
    fill: none;
}

.axis path,
.axis line {
    fill: none;
    stroke: grey;
    stroke-width: 1;
    shape-rendering: crispEdges;
}

</style>
<body>
<select name="inSel" id="inSel" onchange=preloadData(this.value);>
      <option value="" selected="selected">-----</option>
  <?php 
       foreach(glob(dirname(__FILE__) . '/data/*csv') as $filename){
       $filename = basename($filename);
       echo "<option value='data/" . $filename . "'>".$filename."</option>";
    }
?>

</select>

</body>
</html>
