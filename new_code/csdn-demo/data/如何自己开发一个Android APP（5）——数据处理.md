# 如何自己开发一个Android APP（5）——数据处理

Android应用中的数据存储选项共有五种主要类型：将数据保存在应用的共享偏好当中、保存在内部存储（专属于应用本身）当中、保存在外部存储（向设备公开）当中、保存在数据库当中以及保存在可通过设备互联网连接访问的Web资源当中。

共享偏好
----

共享偏好允许以键-值对的形式保存基本数据类型。应用程序的共享偏好文件通常被视为最简单的数据存储选项，但从本质上说它对于存储对象提出了一定程度的限制。

内部存储
----

将文件保存在用户设备的内部以及外部存储当中。如果将文件保存在内部存储中，Android系统会将其视为专属于当前应用的私有数据。这类文件基本上属于应用程序的组成部分，我们无法在应用程序之外直接对其进行访问。再有，如果应用程序被移除、这些文件也会同时被清空。

外部存储
----

只要用户设备支持，我们的应用程序也可以将文件保存在外部存储当中。外部存储种类繁多，包括SD卡、其它便携式介质或者用户无法移除但被系统认定为外部类型的内存存储机制。当我们将文件保存在外部存储中时，其内容将完全公开、大家也无法以任何方式阻止用户或者其它应用对其进行访问。

数据库
---

Android支持开发人员在应用程序内部创建并访问SQLite数据库。在我们创建一套数据库时，其将作为私有组件单纯服务于相关应用程序。  
在Android应用中利用SQLite数据库的方法多种多样，推荐使用扩展SQLiteOpenHelper的类来实现这方面需求。在该类当中，我们需要定义数据库属性、创建各种类变量（包括我们所定义的数据库列表名称及其SQL创建字符串）

互联网
---

利用用户设备上的互联网连接来存储并检索来自Web的数据，只要网络连接有效、这一机制就能正常运作。为了实现这一目标，我们需要在自己的清单文件中添加“android.permission.INTERNET”权限。  
如果我们希望自己的应用能够从互联网中获取数据，则必须保证这一流程脱离应用主UI线程。利用AsyncTask，可以通过后台进程的方式从Web源获取数据、在数据下载完成后将结果写入UI、最后让UI正常执行自身功能。  
还可以将一个内部AsyncTask类添加到Activity类当中，并在需要获取数据的时候在该Activity中创建一个AsyncTask实例。通过在AsyncTask中引入doInBackground与onPostExecute两种方法，检索Activity中所获取到的数据并将其写入用户界面。

SQLite数据库
---------

由于使用网络数据库，需要购买公用IP之类的，以我的能力还无法满足！所以“委曲求全”，只能把数据存在手机上了。  
使用SQLite数据库并不需要在手机上另外安装一个数据库软件，Android系统已经集成了这个数据库。

### SQLiteOpenHelper

一个抽象类，通过继承该类，然后重写数据库创建以及更新的方法，还可以通过该类的对象获得数据库实例或者关闭数据库。

**创建方法：**

* `onCreate(database)`：首次使用软件时生成数据库表。
* `onUpgrade(database,oldVersion,newVersion)`：在数据库的版本发生变化时会被调用， 一般在软件升级时才需改变版本号，而数据库的版本是由程序员控制的，假设数据库现在的版本是1，由于业务的变更，修改了数据库表结构，这时候就需要升级软件，升级软件时希望更新用户手机里的数据库表结构，为了实现这一目的，可以把原来的数据库版本设置为2 或者其他与旧版本号不同的数字即可。

```
// 自定义一个类继承SQLiteOpenHelper类
public class MyDBOpenHelper extends SQLiteOpenHelper
{
    public MyDBOpenHelper(Context context, String name, CursorFactory factory, int version)
    {
    	// 在该类的构造方法super中设置好要创建的数据库名、版本号
    	super(context, "my.db", null, 1); 
    }

    //数据库第一次创建时被调用    
    @Override
    public void onCreate(SQLiteDatabase db) 
    {
        db.execSQL("CREATE TABLE person(personid INTEGER PRIMARY KEY AUTOINCREMENT,name VARCHAR(20))");
        
    }
    
    //软件版本号发生改变时调用
    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion)
    {
        db.execSQL("ALTER TABLE person ADD phone VARCHAR(12) NULL");
    }
}
```

调用数据库对象的`getWritableDatabase()`方法，即可创建数据库（返回值为SQLiteDatabase类型）。

### SQLiteDatabase和Cursor

SQLiteDatabase：数据库访问类，可以通过该类的对象来对数据库做一些增删改查的操作。  
Cursor：游标，类似于JDBC里的resultset结果集，可以简单理解为指向数据库中某一个记录的指针！

**增删改查的方法：**

```
public class MainActivity extends AppCompatActivity implements View.OnClickListener
{

    private Context mContext;
    private Button btn_insert; // 增
    private Button btn_delete; // 删
    private Button btn_update; // 改
    private Button btn_query; // 查
    
    private SQLiteDatabase db;
    private MyDBOpenHelper myDBHelper;
    private StringBuilder sb;
    private int i = 1;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        mContext = MainActivity.this;
        myDBHelper = new MyDBOpenHelper(mContext, "my.db", null, 1);
        bindViews();
    }

    private void bindViews() {
        btn_insert = (Button) findViewById(R.id.btn_insert);
        btn_delete = (Button) findViewById(R.id.btn_delete);
        btn_update = (Button) findViewById(R.id.btn_update);
        btn_query = (Button) findViewById(R.id.btn_query);

        btn_insert.setOnClickListener(this);
        btn_delete.setOnClickListener(this);
        btn_update.setOnClickListener(this);
        btn_query.setOnClickListener(this);
    }

    @Override
    public void onClick(View v) 
    {
        db = myDBHelper.getWritableDatabase();
        switch (v.getId())
        {
            case R.id.btn_insert:
                ContentValues values1 = new ContentValues();
                // ContentValues类和Hashtable比较类似，它也是负责存储一些名值对，但是它存储的名值对当中的名是一个String类型，而值都是基本类型。
                values1.put("name", "第" + i + "个人");
                i++;
                // insert()参数依次是：表名，强行插入null值得数据列的列名，一行记录的数据
                db.insert("person", null, values1);
                Toast.makeText(mContext, "插入完毕~", Toast.LENGTH_SHORT).show();
                break;
			
			case R.id.btn_delete:
                // 参数依次是表名，以及where条件与约束
                db.delete("person", "personid = ?", new String[]{"3"});
                break;

			case R.id.btn_update:
                ContentValues values2 = new ContentValues();
                values2.put("name", "张三");
                // 参数依次是表名，修改后的值，where条件，以及约束。如果不指定第三个、第四个参数，会更改所有行。
                db.update("person", values2, "name = ?", new String[]{"第3个人"});
                break;
            
            case R.id.btn_query:
                sb = new StringBuilder();
                // 参数依次是：表名，列名，where约束条件，where中占位符提供具体的值，指定group by的列，进一步约束。
                //指定查询结果的排序方式
                Cursor cursor = db.query("person", null, null, null, null, null, null);
                if (cursor.moveToFirst())
                {
                    do
                    {
                        int pid = cursor.getInt(cursor.getColumnIndex("personid"));
                        String name = cursor.getString(cursor.getColumnIndex("name"));
                        sb.append("id：" + pid + "：" + name + "\n");
                    } while (cursor.moveToNext());
                }
                cursor.close();
                Toast.makeText(mContext, sb.toString(), Toast.LENGTH_SHORT).show();
                break;
        }
    }
}
```

**使用SQL语句操作的方法：**

* `execSQL(SQL,Object[])`：使用带占位符的SQL语句，这个是执行修改数据库内容的sql语句用的（增、删、改操作）。
* `rawQuery(SQL,Object[])`：使用带占位符的SQL查询操作（查询操作）。
* Cursor对象移动指针的方法：  
  `move(offset)`：指定向上或者向下移动的行数，整数表示向下移动，负数表示向上移动。  
  `moveToFirst()`：指针移动到第一行，成功则返回true（同时说明有数据）。  
  `moveToLast()`：指针移动到最后一行，成功则返回true。  
  `moveToNext()`：指针移动到下一行，成功则返回true（表明还有元素）。  
  `moveToPrevious()`：移动到上一条记录。  
  `getCount( )`：获得总得数据条数。  
  `isFirst()`：是否为第一条记录。  
  `isLast()`：是否为最后一项。  
  `moveToPosition(int)`：移动到指定行。

```
// 插入数据：
public void save(Person p)
{
    SQLiteDatabase db = dbOpenHelper.getWritableDatabase();
    db.execSQL("INSERT INTO person(name,phone) values(?,?)", new String[]{p.getName(),p.getPhone()});
}
// 删除数据：
public void delete(Integer id)
{
    SQLiteDatabase db = dbOpenHelper.getWritableDatabase();
    db.execSQL("DELETE FROM person WHERE personid = ?", new String[]{id});
}
// 修改数据：
public void update(Person p)
{
    SQLiteDatabase db = dbOpenHelper.getWritableDatabase();
    db.execSQL("UPDATE person SET name = ?,phone = ? WHERE personid = ?", new String[]{p.getName(),p.getPhone(),p.getId()});
}
// 查询数据：
public Person find(Integer id)
{
    SQLiteDatabase db = dbOpenHelper.getReadableDatabase();
    Cursor cursor =  db.rawQuery("SELECT * FROM person WHERE personid = ?", new String[]{id.toString()});
    //存在数据才返回true
    if(cursor.moveToFirst())
    {
        int personid = cursor.getInt(cursor.getColumnIndex("personid"));
        String name = cursor.getString(cursor.getColumnIndex("name"));
        String phone = cursor.getString(cursor.getColumnIndex("phone"));
        return new Person(personid,name,phone);
    }
    cursor.close();
    return null;
}
// 数据分页：
public List<Person> getScrollData(int offset,int maxResult)
{
    List<Person> person = new ArrayList<Person>();
    SQLiteDatabase db = dbOpenHelper.getReadableDatabase();
    Cursor cursor =  db.rawQuery("SELECT * FROM person ORDER BY personid ASC LIMIT= ?,?",
        new String[]{String.valueOf(offset),String.valueOf(maxResult)});
    while(cursor.moveToNext())
    {
        int personid = cursor.getInt(cursor.getColumnIndex("personid"));
        String name = cursor.getString(cursor.getColumnIndex("name"));
        String phone = cursor.getString(cursor.getColumnIndex("phone"));
        person.add(new Person(personid,name,phone)) ;
    }
    cursor.close();
    return person;
}
// 查询记录数：
public long getCount()
{
    SQLiteDatabase db = dbOpenHelper.getReadableDatabase();
    Cursor cursor =  db.rawQuery("SELECT COUNT (*) FROM person",null);
    cursor.moveToFirst();
    long result = cursor.getLong(0);
    cursor.close();
    return result;      
}
```