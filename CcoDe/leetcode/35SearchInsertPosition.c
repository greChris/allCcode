int searchInsert(int* nums, int n, int target)
{
    int arxi = 0;
    int telos = n -1;
    int mesi;

    while (arxi <= telos)
    {
        mesi = arxi+ (telos -arxi) / 2;

        if (nums[mesi] == target)
        {
            return mesi;
        }

        else if (nums[mesi] < target)
        {
            arxi = mesi + 1;
        }

        else
        {
            telos = mesi- 1;
        }
    }
    return arxi;
}
