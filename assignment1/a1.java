import java.io.IOException;
import java.util.Arrays;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class a1 {
  //Pairing mapper is the second mapper, it takes in the data from output_map1
  public static class PairingMapper extends Mapper<Object, Text, IntWritable, IntWritable>{
    private static IntWritable a = new IntWritable();
    private static IntWritable b = new IntWritable();

    //main map function
    public void map(Object k, Text vs, Context context) throws IOException, InterruptedException{
      String[] values = vs.toString().split("\\s");
      //getting the key as it is the first value 
      int key = Integer.parseInt(values[0]);
      //loop through values
      for(int i = 1; i<values.length; i++){
        int val = Integer.parseInt(values[i]);
        //negative values are the original ones and we want to keep these
        if(val < 0){
          a.set(key);
          b.set(val);
          context.write(a, b);
        }
        //for positive values, these are the "mirrored" values followers -> followees
        else{
          //send all combinations, these combinations are followers(or followed by) of KEY
          for(int j = i+1; j < values.length; j++){
            int valb = Integer.parseInt(values[j]);
            if(valb > 0){
              a.set(val);
              b.set(valb);
              context.write(a,b);
              context.write(b,a);
            }
          }
        }
      }
    }
  }
  //2nd reducer
  public static class PairingReducer extends Reducer<IntWritable, IntWritable, IntWritable, Text>{
    private static Text data = new Text();

    //reducer function, takes in all values and prints to output
    public void reduce(IntWritable key, Iterable<IntWritable> value, Context context) throws IOException, InterruptedException{
      String vals = new String();
      String list = new String();
      //sum will be the value of number of same followers
      int sum = 0;
      //geting a array from the iterable cause they suck/i dont know how they work
      for (IntWritable val: value){
        vals += val.get()+" ";
      }
      //get string array
      String[] values = vals.toString().split("\\s");
      for (int i = 0; i < values.length; i++){
        int a = Integer.parseInt(values[i]);
        //for pos values check if no originals
        if(a>0){
          sum = contains(values, a);
          //if no originals save values to context
          if(a!=0 && a>0 && sum > 0){
            //if no orginals fake the original value to not count again
            values[i]= Integer.toString(a*-1);
            list = list+(a+"("+sum+") ");
            sum = 0;
          }
        }
        
      }
      //data.set(vals);
      data.set(sort(list));
      context.write(key, data);
    }
    //function to check if array of values has int A and to count the values if they are positive
    private int contains(String[] values, int a){
      int sum = 0;
      for (int j = 0; j < values.length; j++){
        int b = Integer.parseInt(values[j]);
        if (a==b){
          sum++;
        }
        else if (a*-1 == b){
          return 0;
        }
      }
      return sum;
    }
    //sorts the values by highest sum
    private String sort(String lists){
      String[] values = lists.toString().split("\\s");
      int max;
      String tmp = new String();
      for (int i =0; i < values.length; i++){
        max = i;
        for (int j = i+1; j < values.length; j++){
          if(getSum(values[j]) > getSum(values[max]))max = j;
        }
        if(i !=max){
          tmp = values[i];
          values[i] = values[max];
          values[max] = tmp;
        }
      }
      tmp = "";
      for (int i =0; i < values.length; i++){
        tmp += values[i]+" ";
      }
      return tmp;
    }
    //gets the sum from the string X(SUM)
    private int getSum(String a){
      return Integer.parseInt(a.substring(a.indexOf('(')+1,a.indexOf(')')));
    }
  }

  //first mapper
  public static class IndexMapper extends Mapper<Object, Text, IntWritable, IntWritable>{
    private static IntWritable a = new IntWritable();
    private static IntWritable b = new IntWritable();
    private static IntWritable c = new IntWritable();
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
      String[] values = value.toString().split("\\s");
      b.set(Integer.parseInt(values[0]));
      for(int i = 1; i < values.length; i++){

        a.set(Integer.parseInt(values[i])*-1);
        c.set(Integer.parseInt(values[i]));
        context.write(b, a);
        context.write(c, b);
      }
    }
  }
  public static class IndexReducer extends Reducer<IntWritable, IntWritable, IntWritable, Text>{
    private static Text data = new Text();
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{
      String list = new String();
      for (IntWritable val: values){
        list += val.get()+" ";
      }
      data.set(list);
      context.write(key, data);
    }
  }
  public static void main(String[] args) throws Exception{
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "a1p1");
    job.setJarByClass(a1.class);
    job.setMapperClass(IndexMapper.class);
    job.setReducerClass(IndexReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path("output_map1"));
    if(job.waitForCompletion(true)){
    conf = new Configuration();
    job = Job.getInstance(conf, "a1p2");
    job.setJarByClass(a1.class);
    job.setMapperClass(PairingMapper.class);
    job.setReducerClass(PairingReducer.class);
    job.setOutputKeyClass(IntWritable.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path("output_map1"+"/part-r-00000"));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0: 1);
    }
  }
}
