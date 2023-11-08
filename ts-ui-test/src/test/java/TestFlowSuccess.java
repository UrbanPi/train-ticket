import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Random;
import java.util.concurrent.TimeUnit;

public class TestFlowSuccess {
    private WebDriver driver;
    private String baseUrl;

    public static String getRandomString(int length) {
        String KeyString = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
        StringBuffer sb = new StringBuffer();
        int len = KeyString.length();
        for (int i = 0; i < length; i++) {
            sb.append(KeyString.charAt((int) Math.round(Math.random() * (len - 1))));
        }
        return sb.toString();
    }

    public static void login(WebDriver driver,String username,String password){

        //Add random delay to emulate the waiting between user click
        try{
            Thread.sleep(new Random().nextInt(7000) + 3000);
        }catch(Exception e){
            e.printStackTrace();
        }
        driver.findElement(By.id("flow_four_page")).click();
        driver.findElement(By.id("flow_advance_reserve_login_email")).clear();
        driver.findElement(By.id("flow_advance_reserve_login_email")).sendKeys(username);
        driver.findElement(By.id("flow_advance_reserve_login_password")).clear();
        driver.findElement(By.id("flow_advance_reserve_login_password")).sendKeys(password);
        driver.findElement(By.id("flow_advance_reserve_login_button")).click();
    }

    @BeforeClass
    public void setUp() throws Exception {
        System.setProperty("webdriver.chrome.driver", "F:/gitwork/chromedriver.exe");
        driver = new ChromeDriver();
        baseUrl = "http://10.141.212.21";
        driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
    }

    @Test
    //Test Flow Preserve Step 1: - Login
    public void testLogin()throws Exception{

        driver.get(baseUrl + "/");

        //define username and password
        String username = "fdse_microservices@163.com";
        String password = "DefaultPassword";

        //call function login
        login(driver,username,password);
        Thread.sleep(1000);

        //get login status
//        String statusLogin = driver.findElement(By.id("flow_preserve_login_msg")).getText();
//        if("".equals(statusLogin)) {
//            System.out.println("Failed to Login! Status is Null!");
//        } else if(statusLogin.startsWith("Success")) {
//            System.out.println("Success to Login! Status:" + statusLogin);
//        } else {
//            System.out.println("Failed to Login! Status:" + statusLogin);
//        }
//        Assert.assertEquals(statusLogin.startsWith("Success"),true);
//
//        Thread.sleep(1000);
//        String js = "document.getElementById('flow_two_page').scrollIntoView(false)";
//        ((JavascriptExecutor)driver).executeScript(js);
//        Thread.sleep(1000);
//
//        driver.findElement(By.id("flow_two_page")).click();
    }

    @Test (dependsOnMethods = {"testLogin"})
    //test Flow Preserve Step 2: - Ticket Booking
    public void testBooking() throws Exception{
        //locate booking startingPlace input
        WebElement elementBookingStartingPlace = driver.findElement(By.id("flow_advance_reserve_startingPlace"));
        elementBookingStartingPlace.clear();
        elementBookingStartingPlace.sendKeys("Shang Hai");

        //locate booking terminalPlace input
        WebElement elementBookingTerminalPlace = driver.findElement(By.id("flow_advance_reserve_terminalPlace"));
        elementBookingTerminalPlace.clear();
        elementBookingTerminalPlace.sendKeys("Nan Jing");

        //locate booking Date input
        String bookDate = "";
        SimpleDateFormat sdf=new SimpleDateFormat("yyyy-MM-dd");
        Calendar newDate = Calendar.getInstance();
        Random randDate = new Random();
        int randomDate = randDate.nextInt(26);
        newDate.add(Calendar.DATE, randomDate+5);
        bookDate=sdf.format(newDate.getTime());

        JavascriptExecutor js = (JavascriptExecutor) driver;
        js.executeScript("document.getElementById('flow_advance_reserve_booking_date').value='"+bookDate+"'");

        //locate Train Type input
        WebElement elementBookingSearchType = driver.findElement(By.id("flow_advance_reserve_select_searchType"));
        Select selTraintype = new Select(elementBookingSearchType);
        selTraintype.selectByValue("1"); //ALL

        //locate Train search button
        WebElement elementBookingSearchBtn = driver.findElement(By.id("flow_advance_reserve_booking_button"));


        //Add random delay to emulate the waiting between user click
        Thread.sleep(new Random().nextInt(7000) + 3000);
        elementBookingSearchBtn.click();

        Thread.sleep(new Random().nextInt(7000) + 3000);
        elementBookingSearchBtn.click();

//        List<WebElement> ticketsList = driver.findElements(By.xpath("//table[@id='tickets_booking_list_table']/tbody/tr"));
//        //Confirm ticket selection
//        if (ticketsList.size() == 0) {
//
//            //Add random delay to emulate the waiting between user click
//            Thread.sleep(new Random().nextInt(7000) + 3000);
//            elementBookingSearchBtn.click();
//
//            ticketsList = driver.findElements(By.xpath("//table[@id='tickets_booking_list_table']/tbody/tr"));
//        }
//        if(ticketsList.size() > 0) {
//            //Pick up a train at random and book tickets
//            System.out.printf("Success to search tickets，the tickets list size is:%d%n",ticketsList.size());
//            Random rand = new Random();
//            int i = rand.nextInt(1000) % ticketsList.size();
//            WebElement elementBookingSeat = ticketsList.get(i).findElement(By.xpath("td[10]/select"));
//            Select selSeat = new Select(elementBookingSeat);
//            selSeat.selectByValue("3"); //2st
//
//            //Add random delay to emulate the waiting between user click
//            Thread.sleep(new Random().nextInt(7000) + 3000);
//            ticketsList.get(i).findElement(By.xpath("td[13]/button")).click();
//
//            Thread.sleep(1000);
//        }
//        else
//            System.out.println("Tickets search failed!!!");
//        Assert.assertEquals(ticketsList.size() > 0,true);
    }




    @AfterClass
    public void tearDown() throws Exception {
        driver.quit();
    }
}
