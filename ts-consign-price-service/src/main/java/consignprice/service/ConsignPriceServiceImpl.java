package consignprice.service;

import consignprice.domain.ConstFormat;
import consignprice.domain.GetPriceDomain;
import consignprice.domain.PriceConfig;
import consignprice.repository.ConsignPriceConfigRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.DecimalFormat;

@Service
public class ConsignPriceServiceImpl implements ConsignPriceService {
    @Autowired
    private ConsignPriceConfigRepository repository;

    @Override
    public String getPriceByWeightAndRegion(GetPriceDomain domain) {
        System.out.println(String.format("Receive the request to calculate the price. [%s]", domain.toString()));
        String result;

        PriceConfig priceConfig = repository.findByIndex(0);
        int country = domain.getCountry();
        double initialPrice = priceConfig.getInitialPrice();
        if(domain.getWeight() <= priceConfig.getInitialWeight()){
            result = formatNumber(initialPrice,country);
        }
        else{
            double extraWeight = domain.getWeight() - priceConfig.getInitialWeight();
            if(domain.isWithinRegion())
                result = formatNumber(initialPrice + extraWeight * priceConfig.getWithinPrice(),country);
            else
                result = formatNumber(initialPrice + extraWeight * priceConfig.getBeyondPrice(),country);
        }
        System.out.println(String.format("Calculate the consign price successfully. The price is [%s]", result));
        return result;
    }

    //Change the format of price
    private String formatNumber(double price, int format){
        DecimalFormat formatter = new DecimalFormat("#,###.00");
        String temp = formatter.format(price);
        String ret;
        switch (format){
            case ConstFormat.FRENCH_FORMAT :
                ret = "₣" + temp.replace(","," ");;
                break;
            case ConstFormat.GERMAN_FORMAT:
                temp = temp.replace("."," ");
                temp = temp.replace(",",".");
                temp = temp.replace(" ",",");
                ret = "€" + temp;
                break;
            default:
                ret = "$" + temp;
                break;
        }
        return ret;
    }

    @Override
    public String queryPriceInformation() {
        StringBuilder sb = new StringBuilder();
        PriceConfig price = repository.findByIndex(0);
        sb.append("The price of weight within ");
        sb.append(price.getInitialWeight());
        sb.append(" is ");
        sb.append(price.getInitialPrice());
        sb.append(". The price of extra weight within the region is ");
        sb.append(price.getWithinPrice());
        sb.append(" and beyond the region is ");
        sb.append(price.getBeyondPrice());
        sb.append("\n");
        return sb.toString();
    }

    @Override
    public boolean createAndModifyPrice(PriceConfig config) {
        System.out.println("[Consign Price Service][Create New Price Config]");

        PriceConfig originalConfig;
        if(repository.findByIndex(0) != null)
            originalConfig = repository.findByIndex(0);
        else
            originalConfig = new PriceConfig();
        originalConfig.setId(config.getId());
        originalConfig.setIndex(0);
        originalConfig.setInitialPrice(config.getInitialPrice());
        originalConfig.setInitialWeight(config.getInitialWeight());
        originalConfig.setWithinPrice(config.getWithinPrice());
        originalConfig.setBeyondPrice(config.getBeyondPrice());
        repository.save(originalConfig);
        return true;
    }

    @Override
    public PriceConfig getPriceConfig() {
        return repository.findByIndex(0);
    }
}
