package org.uwplse.dbreaker;

import com.mysql.jdbc.jdbc2.optional.MysqlDataSource;
import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;
import org.apache.calcite.adapter.jdbc.JdbcSchema;
import org.apache.calcite.jdbc.CalciteConnection;
import org.apache.calcite.schema.Schema;
import org.apache.calcite.schema.SchemaPlus;
import org.apache.commons.dbcp.BasicDataSource;
import org.json.JSONArray;
import org.json.JSONObject;

import javax.sql.DataSource;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;
import java.util.Scanner;


/**
 * Created by clwang on 5/25/18.
 */
public class CalciteInterface {
    // JDBC driver name and database URL

    public static List<String> simpleScriptParser(String content) {
        content = content.trim();
        List<String> result = new ArrayList<String>();
        String[] statements = content.split(";");
        for (String s : statements) {
            String stripped = s.trim();
            if (stripped != "")
                result.add(stripped);
        }
        return result;
    }

    public static List<String> readFileContent(String fileName) throws FileNotFoundException {
        // read queries from the file
        List<String> result = new ArrayList<String>();
        File file = new File(fileName);
        Scanner sc = new Scanner(file);
        while (sc.hasNextLine())
            result.add(sc.nextLine());
        return result;
    }

    public static void main(String[] args)
            throws ClassNotFoundException, SQLException, ArgumentParserException, IOException {

        ArgumentParser parser = ArgumentParsers.newFor("db_tools")
                .build().description("The tool to connect Calcite to MySQL.");

        parser.addArgument("--database").metavar("DATABASE").setDefault("test_db");
        parser.addArgument("--user").metavar("USERNAME").setDefault("dbtest");
        parser.addArgument("--password").metavar("PASSWORD").setDefault("dbtest");
        parser.addArgument("--input-file").metavar("INPUT_FILE");
        parser.addArgument("--output-file").metavar("OUTPUT_FILE");

        Namespace arguments = parser.parseArgs(args);

        //  Database information and credentials
        final String DB_NAME = arguments.get("database");
        //final String DB_URL = "jdbc:mysql://localhost:3306/" + DB_NAME;
        final String USER = arguments.get("user");
        final String PASS = arguments.get("password");
        final String inputFile = arguments.get("input_file");
        final String outputFile = arguments.get("output_file");

        System.out.println(DB_NAME + " " + USER + " " + PASS + " " + inputFile);

        List<String> ddlContent = new ArrayList<>();
        List<String> queryContent = new ArrayList<>();

        boolean ddlMode = true;
        for (String s : readFileContent(inputFile)) {
            if (s.startsWith("---------- [DDL]")) {
                ddlMode = true;
            }
            if (s.startsWith("---------- [Queries]"))
                ddlMode = false;

            if (ddlMode) {
                ddlContent.add(s);
            } else {
                queryContent.add(s);
            }
        }

        List<String> ddlCommands = simpleScriptParser(String.join(" ", ddlContent));
        List<String> queries = simpleScriptParser(String.join(" ", queryContent));

        MysqlDataSource mysqlDataSource = new MysqlDataSource();
        mysqlDataSource.setUser(USER);
        mysqlDataSource.setPassword(PASS);
        mysqlDataSource.setServerName("localhost");
        mysqlDataSource.setDatabaseName(DB_NAME);
        mysqlDataSource.setUseSSL(false);

        Connection conn = mysqlDataSource.getConnection();
        Statement ddlStatement = conn.createStatement();
        // execute ddl
        for (String q : ddlCommands) {
            ddlStatement.execute(q);
        }
        conn.close();



        Properties info = new Properties();
        info.setProperty("lex", "JAVA");
        Connection connection = DriverManager.getConnection("jdbc:calcite:", info);
        CalciteConnection calciteConnection = connection.unwrap(CalciteConnection.class);
        SchemaPlus rootSchema = calciteConnection.getRootSchema();

        // create schema
        MysqlDataSource calciteDataSource = new MysqlDataSource();
        calciteDataSource.setServerName("localhost");
        calciteDataSource.setUser(USER);
        calciteDataSource.setPassword(PASS);
        calciteDataSource.setDatabaseName(DB_NAME);
        calciteDataSource.setUseSSL(false);
        Schema schema = JdbcSchema.create(rootSchema, "test_db", calciteDataSource, null, "test_db");

        rootSchema.add("test_db", schema);
        Statement statement = calciteConnection.createStatement();

        // execute query
        for (String q : queries) {
            ResultSet rs = statement.executeQuery(q.replace(";", ""));
            String resultJson = resultToJsonStr(rs);
            if (outputFile != null) {
                FileWriter fw = new FileWriter(new File(outputFile));
                fw.write(resultJson);
            } else {
                System.out.println(resultJson);
            }
            rs.close();
        }

        statement.close();
        connection.close();

    }

    private static String resultToJsonStr(ResultSet resultSet) throws SQLException {

        JSONObject output = new JSONObject();
        JSONArray content = new JSONArray();

        final ResultSetMetaData metaData = resultSet.getMetaData();
        final int columnCount = metaData.getColumnCount();

        List<String> columnTypes = new ArrayList<String>();
        List<String> columnNames = new ArrayList<String>();
        for (int i = 1; i <= columnCount; i ++) {
            columnNames.add(metaData.getColumnLabel(i));
            columnTypes.add(metaData.getColumnTypeName(i));
        }
        output.put("header", columnNames);
        output.put("type", columnTypes);

        while (resultSet.next()) {
            JSONArray row = new JSONArray();
            for (int i = 1; i <= columnCount; i++) {
                row.put(resultSet.getObject(i));
            }
            content.put(row);
        }
        output.put("content", content);
        return output.toString();
    }
}
