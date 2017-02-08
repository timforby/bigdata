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
  public static class PairingMapper extends Mapper<Object, Text, Text, IntWritable>{
    public void map(Object k, Text vs, Context context) throws IOException, InterruptedException{
      String[] values = vs.toString().split("\\s");
      int key = Integer.parseInt(values[0]);
      for(int i = 1; i<values.length; i++){
        String data = new String(" ");
        int val = Integer.parseInt(values[i]);
        if(val < 0 && !hasNeg(val,values)){
          data = key+","+(val*-1);
        }
        else if(val >0 && hasNeg(val,values)){
          data = val+","+key;
        }
        for(int j = 1; j < values.length; j++){
          int v = Integer.parseInt(values[j]);
          if(v > 0)context.write(new Text(data),new IntWritable(v));
        }
      }
    }
    private boolean hasNeg(int val, String[] values){
      for(int i = 1; i < values.length; i++){
        if(Integer.parseInt(values[i])*(-1) == val)return true;
      }
      return false;
    }
  }
  public static class IndexMapper extends Mapper<Object, Text, IntWritable, IntWritable>{
    private static IntWritable a = new IntWritable();
    private static IntWritable b = new IntWritable();
    private static IntWritable c = new IntWritable();
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException{
      String[] values = value.toString().split("\\s");
      b.set(Integer.parseInt(values[0]));
      c.set(-1 * Integer.parseInt(values[0]));
      for(int i = 1; i < values.length; i++){

        a.set(Integer.parseInt(values[i]));
        context.write(b, a);
        context.write(a, c);
      }
    }
  }
  public static class IndexReducer extends Reducer<IntWritable, IntWritable, IntWritable, Text>{
    private static Text data = new Text();
    public void reduce(IntWritable key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{
      String list = new String(key.get()+" ");
      for (IntWritable val: values){
        list += val.get()+" ";
      }
      data.set(list);
      context.write(key, data);
    }
  }
  public static class PairingReducer extends Reducer<Text, IntWritable, Text, Text>{
    private static Text data = new Text();
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException{
      String follower = new String();
      int sum = 0;
      for (IntWritable val: values){
        for(IntWritable v:values){
          if (val.get() == v.get())sum++;
        }
      }
      String list = new String(key.toString()+": "+sum);
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
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    if(job.waitForCompletion(true)){
    conf = new Configuration();
    job = Job.getInstance(conf, "a1p2");
    job.setJarByClass(a1.class);
    job.setMapperClass(PairingMapper.class);
    job.setReducerClass(PairingReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[1]+"/part-r-00000"));
    FileOutputFormat.setOutputPath(job, new Path(args[2]));
    System.exit(job.waitForCompletion(true) ? 0: 1);
    }
  }
}
